from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.template.response import TemplateResponse
import os
from .models import (
    Profile, Task, Question, LearningMaterial,
    Contact, Enrollment, ClientRequest, Project, Announcement,
    InternshipPricing, ProjectSubmission,
    DailyChallengeTask, DailyCheckIn, UserStreak,
    ChallengeTrack, UserChallengeEnrollment, DailyTrackCheckIn, MilestoneAchievement,
    ClientProfile, ClientProject, ClientProjectMilestone,
    ClientProjectDeliverable, ClientProjectUpdate, ClientInvoice,
    EmailTemplate, OFFER_LETTER_PLACEHOLDERS, CREDENTIALS_PLACEHOLDERS,
    Review,
)

# ===========================================================
# Site Header Customization
# ===========================================================
admin.site.site_header = "TRHvision Admin Panel"
admin.site.site_title  = "TRHvision"
admin.site.index_title = "Content Management"


# ===========================================================
# Helper Inlines
# ===========================================================
class LearningMaterialInline(admin.StackedInline):
    model = LearningMaterial
    extra = 1
    fields = ('title', 'content', 'video_url', 'file', 'week_number', 'order')


def _docx_to_html(docx_file, media_root):
    """Convert an in-memory docx upload to HTML, saving embedded images to media."""
    from docx import Document
    from docx.document import Document as _Document
    from docx.oxml.text.paragraph import CT_P
    from docx.oxml.table import CT_Tbl
    from docx.table import _Cell, Table
    from docx.text.paragraph import Paragraph
    from docx.oxml.ns import qn
    import base64, uuid, os

    document = Document(docx_file)
    # Build a map of rId → image bytes for embedded images
    image_map = {}
    for rel in document.part.rels.values():
        if 'image' in rel.reltype:
            try:
                img_bytes = rel.target_part.blob
                ext = rel.target_part.content_type.split('/')[-1]  # e.g. 'png', 'jpeg'
                fname = f"{uuid.uuid4().hex}.{ext}"
                save_dir = os.path.join(media_root, 'uploads', 'docx_images')
                os.makedirs(save_dir, exist_ok=True)
                fpath = os.path.join(save_dir, fname)
                with open(fpath, 'wb') as f:
                    f.write(img_bytes)
                image_map[rel.rId] = f"/media/uploads/docx_images/{fname}"
            except Exception:
                pass

    def iter_block_items(parent):
        if isinstance(parent, _Document):
            parent_elm = parent.element.body
        elif isinstance(parent, _Cell):
            parent_elm = parent._tc
        else:
            return
        for child in parent_elm.iterchildren():
            if isinstance(child, CT_P):
                yield Paragraph(child, parent)
            elif isinstance(child, CT_Tbl):
                yield Table(child, parent)

    def process_paragraph(para):
        style = para.style.name.lower() if para.style else ''
        para_xml = para._p
        
        # Check for inline images
        inline_imgs = para_xml.findall('.//' + qn('a:blip'))
        
        # Check for textboxes (drawings containing text)
        txbx_paras = para_xml.findall('.//' + qn('w:txbxContent') + '//' + qn('w:p'))
        
        res_html = ""
        
        # Extract text excluding textboxes
        text_parts = []
        for run in para.runs:
            if not run._r.findall('.//' + qn('w:txbxContent')):
                text_parts.append(run.text)
        text = "".join(text_parts).strip()
        
        if inline_imgs:
            for blip in inline_imgs:
                rId = blip.get(qn('r:embed'))
                if rId and rId in image_map:
                    res_html += f'<p><img src="{image_map[rId]}" style="max-width:100%;height:auto;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.1);" alt="Image"></p>'
            if not text and not txbx_paras:
                return res_html

        if txbx_paras:
            res_html += '<div style="border-left: 5px solid #0ea5e9; padding: 1.5rem 2rem; margin: 2rem 0; border-radius: 0 12px 12px 0; background: linear-gradient(145deg, #f8fafc, #f1f5f9); box-shadow: 0 4px 15px rgba(0,0,0,0.04);">'
            for tp in txbx_paras:
                tp_obj = Paragraph(tp, para._parent)
                res_html += process_paragraph(tp_obj)
            res_html += '</div>'
            if not text:
                return res_html

        if not text:
            return res_html if res_html else ''

        if 'heading 1' in style:
            res_html += f'<h2>{text}</h2>'
        elif 'heading 2' in style:
            res_html += f'<h3>{text}</h3>'
        elif 'heading 3' in style:
            res_html += f'<h4>{text}</h4>'
        elif 'list bullet' in style:
            res_html += f'<ul><li>{text}</li></ul>'
        elif 'list number' in style:
            res_html += f'<ol><li>{text}</li></ol>'
        else:
            run_html = ''
            for run in para.runs:
                if run._r.findall('.//' + qn('w:txbxContent')):
                    continue
                t = run.text
                if not t: continue
                t = t.replace("<", "&lt;").replace(">", "&gt;")
                if run.bold:
                    t = f'<strong>{t}</strong>'
                if run.italic:
                    t = f'<em>{t}</em>'
                if run.underline:
                    t = f'<u>{t}</u>'
                run_html += t
            res_html += f'<p>{run_html}</p>'
            
        return res_html

    html_parts = []
    for block in iter_block_items(document):
        if isinstance(block, Paragraph):
            html_parts.append(process_paragraph(block))
        elif isinstance(block, Table):
            html_parts.append('<div class="table-responsive" style="margin: 2rem 0; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #e2e8f0; overflow: hidden;"><table class="table mb-0" style="width:100%; border-collapse: collapse;">')
            for r_idx, row in enumerate(block.rows):
                bg = "#fbfcfd" if r_idx % 2 != 0 else "#ffffff"
                html_parts.append(f'<tr style="background:{bg};">')
                for cell in row.cells:
                    html_parts.append('<td style="border-top:1px solid #e2e8f0; border-right:1px solid #e2e8f0; padding:1.25rem; vertical-align:top;">')
                    for cell_block in iter_block_items(cell):
                        if isinstance(cell_block, Paragraph):
                            html_parts.append(process_paragraph(cell_block))
                    html_parts.append('</td>')
                html_parts.append('</tr>')
            html_parts.append('</table></div>')

    return '\n'.join(html_parts)


def _auto_extract_docx(obj):
    """
    Auto-populate content from .docx if file is a Word document.
    Handles both InMemoryUploadedFile (new upload) and FieldFile (saved on disk).
    """
    from django.conf import settings as django_settings
    import io

    if not obj.file:
        return

    # Get the filename - could be an upload object or a FieldFile path
    raw_file = obj.file
    file_name = getattr(raw_file, 'name', '') or ''
    if not str(file_name).lower().endswith('.docx'):
        return

    try:
        # Case 1: Fresh upload - has read() method (InMemoryUploadedFile / TemporaryUploadedFile)
        if hasattr(raw_file, 'read'):
            raw_file.seek(0)
            file_data = io.BytesIO(raw_file.read())
        else:
            # Case 2: Already saved FieldFile - open from disk
            raw_file.open('rb')
            file_data = io.BytesIO(raw_file.read())
            raw_file.close()

        html = _docx_to_html(file_data, django_settings.MEDIA_ROOT)
        if html.strip():
            obj.content = html
    except Exception as e:
        import traceback
        print(f'[DOCX IMPORT ERROR] {e}\n{traceback.format_exc()}')


@admin.register(LearningMaterial)
class LearningMaterialAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'task', 'week_number', 'order')
    list_filter = ('task', 'week_number')
    search_fields = ('title', 'task__title')

    def save_model(self, request, obj, form, change):
        """Auto-extract .docx content into the content field when a Word file is uploaded."""
        if 'file' in form.changed_data:
            _auto_extract_docx(obj)
            if obj.file and str(obj.file.name).lower().endswith('.docx'):
                messages.info(request, f'Word document content was automatically extracted and saved into the content field for "{obj.title}".')
        super().save_model(request, obj, form, change)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-docx/', self.admin_site.admin_view(self.import_docx_view), name='vision_learningmaterial_import_docx'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['import_docx_url'] = 'import-docx/'
        return super().changelist_view(request, extra_context=extra_context)

    def import_docx_view(self, request):
        from django.conf import settings as django_settings
        context = {
            'tasks': Task.objects.all().order_by('category', 'title'),
            'title': 'Import Study Material from Word',
            'opts': self.model._meta,
        }
        if request.method == 'POST':
            task_id = request.POST.get('task_id')
            title = request.POST.get('title', '').strip()
            week_number = request.POST.get('week_number', 1)
            order = request.POST.get('order', 1)
            docx_file = request.FILES.get('docx_file')

            if not task_id or not title or not docx_file:
                messages.error(request, 'Please fill in all required fields.')
            elif not docx_file.name.endswith('.docx'):
                messages.error(request, 'Only .docx files are supported.')
            else:
                try:
                    html_content = _docx_to_html(docx_file, django_settings.MEDIA_ROOT)
                    task = Task.objects.get(pk=task_id)

                    # ── Duplicate guard ──────────────────────────────────────
                    existing = LearningMaterial.objects.filter(
                        task=task,
                        title=title,
                        week_number=int(week_number),
                    ).first()
                    if existing:
                        messages.warning(
                            request,
                            f'A material titled "{title}" for Week {week_number} already exists '
                            f'under "{task.title}". Import skipped to prevent duplicates. '
                            f'Edit the existing material instead.'
                        )
                        return redirect('../')
                    # ─────────────────────────────────────────────────────────

                    mat = LearningMaterial.objects.create(
                        task=task,
                        title=title,
                        content=html_content,
                        week_number=int(week_number),
                        order=int(order),
                    )
                    messages.success(request, f'Successfully imported "{mat.title}" for task "{task.title}".')
                    return redirect('../')
                except Task.DoesNotExist:
                    messages.error(request, 'Selected task not found.')
                except Exception as e:
                    messages.error(request, f'Import failed: {e}')

        return TemplateResponse(request, 'admin/vision/learningmaterial/import_docx.html', context)

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


# ===========================================================
# Base Task Admin (shared config)
# ===========================================================
class BaseTaskAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category', 'required_period', 'due_date', 'task_link')
    list_filter   = ('category', 'due_date')
    search_fields = ('title', 'description')
    list_editable = ('due_date', 'task_link')
    inlines       = [LearningMaterialInline, QuestionInline]

    def save_formset(self, request, form, formset, change):
        """Hook called after all inline forms are saved. Extract .docx content here."""
        instances = formset.save(commit=False)
        for obj in instances:
            if isinstance(obj, LearningMaterial):
                # Check if a new .docx file was uploaded in this form
                for f in formset.forms:
                    if f.instance == obj or (not obj.pk and f.cleaned_data.get('file')):
                        if 'file' in f.changed_data:
                            uploaded = f.cleaned_data.get('file')
                            if uploaded and hasattr(uploaded, 'name') and str(uploaded.name).lower().endswith('.docx'):
                                obj.file = uploaded
                                _auto_extract_docx(obj)
                                break
            obj.save()
        formset.save_m2m()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self.period_filter:
            return qs.filter(required_period=self.period_filter)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if self.period_filter and 'required_period' in form.base_fields:
            form.base_fields['required_period'].initial = self.period_filter
        return form

    period_filter = None  # Override in subclasses


# ===========================================================
# Proxy Models – Tasks split by period
# ===========================================================
class Task1Month(Task):
    class Meta:
        proxy        = True
        verbose_name = "Task – 1 Month"
        verbose_name_plural = "📗 Tasks – 1 Month"

class Task2Months(Task):
    class Meta:
        proxy        = True
        verbose_name = "Task – 2 Months"
        verbose_name_plural = "📘 Tasks – 2 Months"

class Task3Months(Task):
    class Meta:
        proxy        = True
        verbose_name = "Task – 3 Months"
        verbose_name_plural = "📙 Tasks – 3 Months"

class Task6Months(Task):
    class Meta:
        proxy        = True
        verbose_name = "Task – 6 Months"
        verbose_name_plural = "📕 Tasks – 6 Months"


@admin.register(Task1Month)
class Task1MonthAdmin(BaseTaskAdmin):
    period_filter = 1

@admin.register(Task2Months)
class Task2MonthsAdmin(BaseTaskAdmin):
    period_filter = 2

@admin.register(Task3Months)
class Task3MonthsAdmin(BaseTaskAdmin):
    period_filter = 3

@admin.register(Task6Months)
class Task6MonthsAdmin(BaseTaskAdmin):
    period_filter = 6


# ===========================================================
# Base Project Admin (shared config)
# ===========================================================
class BaseProjectAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category', 'required_period', 'problem_statement')
    list_filter   = ('category',)
    search_fields = ('title', 'description')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self.period_filter:
            return qs.filter(required_period=self.period_filter)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if self.period_filter and 'required_period' in form.base_fields:
            form.base_fields['required_period'].initial = self.period_filter
        return form

    period_filter = None


# ===========================================================
# Proxy Models – Projects split by period
# ===========================================================
class Project1Month(Project):
    class Meta:
        proxy        = True
        verbose_name = "Project – 1 Month"
        verbose_name_plural = "📗 Projects – 1 Month"

class Project2Months(Project):
    class Meta:
        proxy        = True
        verbose_name = "Project – 2 Months"
        verbose_name_plural = "📘 Projects – 2 Months"

class Project3Months(Project):
    class Meta:
        proxy        = True
        verbose_name = "Project – 3 Months"
        verbose_name_plural = "📙 Projects – 3 Months"

class Project6Months(Project):
    class Meta:
        proxy        = True
        verbose_name = "Project – 6 Months"
        verbose_name_plural = "📕 Projects – 6 Months"


@admin.register(Project1Month)
class Project1MonthAdmin(BaseProjectAdmin):
    period_filter = 1

@admin.register(Project2Months)
class Project2MonthsAdmin(BaseProjectAdmin):
    period_filter = 2

@admin.register(Project3Months)
class Project3MonthsAdmin(BaseProjectAdmin):
    period_filter = 3

@admin.register(Project6Months)
class Project6MonthsAdmin(BaseProjectAdmin):
    period_filter = 6


# ===========================================================
# Project Submission Admin
# ===========================================================
@admin.register(ProjectSubmission)
class ProjectSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'submitted_at', 'is_approved')
    list_filter = ('is_approved', 'submitted_at', 'project__category')
    search_fields = ('user__username', 'user__email', 'project__title')
    list_editable = ('is_approved',)
    readonly_fields = ('submitted_at',)

# ===========================================================
# Announcement Admin
# ===========================================================
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display  = ('title', 'period_label', 'short_content', 'is_active', 'created_at')
    list_filter   = ('min_period', 'is_active')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at',)
    list_editable = ('is_active',)

    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content Excerpt'

    def period_label(self, obj):
        labels = {1: '📗 All Interns (1M+)', 2: '📘 2M+ Interns',
                  3: '📙 3M+ Interns',      6: '📕 6M Only'}
        return labels.get(obj.min_period, str(obj.min_period))
    period_label.short_description = 'Visible To'


# ===========================================================
# User + Profile Admin
# ===========================================================
class ProfileInline(admin.StackedInline):
    model             = Profile
    can_delete        = False
    verbose_name_plural = 'Student Profile'

class UserAdmin(BaseUserAdmin):
    inlines      = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_student_id', 'get_internship', 'is_staff')
    list_filter  = BaseUserAdmin.list_filter + ('profile__Intren', 'profile__period')
    search_fields = BaseUserAdmin.search_fields + ('profile__student_id',)

    def get_student_id(self, instance):
        return instance.profile.student_id if hasattr(instance, 'profile') else None
    get_student_id.short_description = 'Student ID'

    def get_internship(self, instance):
        if hasattr(instance, 'profile'):
            return f"{instance.profile.period} - {instance.profile.Intren}"
        return None
    get_internship.short_description = 'Internship'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'Intren', 'period', 'has_certificate')
    list_filter = ('Intren', 'period')
    search_fields = ('user__username', 'user__email', 'student_id')

    def has_certificate(self, obj):
        return bool(obj.certificate)
    has_certificate.boolean = True
    has_certificate.short_description = 'Certificate Generated'


# ===========================================================
# Contact / Client / Enrollment Admin
# ===========================================================
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display  = ('name', 'phone', 'email', 'role', 'subject', 'short_message', 'created_at')
    list_filter   = ('role', 'created_at')
    search_fields = ('name', 'email', 'phone', 'subject', 'message')
    readonly_fields = ('created_at',)

    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message'

@admin.register(ClientRequest)
class ClientRequestAdmin(admin.ModelAdmin):
    list_display  = ('company_name', 'name', 'phone', 'service_type', 'email', 'short_message', 'created_at')
    list_filter   = ('service_type', 'created_at')
    search_fields = ('name', 'company_name', 'phone', 'email', 'message')
    readonly_fields = ('created_at',)

    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display  = ('name', 'college', 'phone', 'domain', 'duration', 'is_paid', 'payment_verification', 'created_at')
    list_filter   = ('domain', 'duration', 'is_paid', 'created_at')
    search_fields = ('name', 'email', 'phone', 'college', 'transaction_id', 'razorpay_order_id', 'razorpay_payment_id')
    readonly_fields = ('created_at',)
    list_editable = ('is_paid',)

    def payment_verification(self, obj):
        if obj.razorpay_payment_id:
            # Generate a clickable link straight to Razorpay Dashboard
            url = f"https://dashboard.razorpay.com/app/payments/{obj.razorpay_payment_id}"
            return format_html('<a href="{}" target="_blank" style="color: blue; text-decoration: underline;">Verify on Razorpay</a><br><small style="color: gray;">ID: {}</small>', url, obj.razorpay_payment_id)
        elif obj.payment_screenshot:
            return format_html('<a href="{}" target="_blank" style="color: green; text-decoration: underline;">View Screenshot</a>', obj.payment_screenshot.url)
        elif obj.transaction_id:
            return format_html('<span style="color: gray;">Txn: {}</span>', obj.transaction_id)
        return format_html('<span style="color: red;">Pending</span>')
    payment_verification.short_description = 'Payment Status / Verification'

    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
            
        return response
    export_as_csv.short_description = "Export Selected as CSV"

# ===========================================================
# Internship Pricing Admin
# ===========================================================
@admin.register(InternshipPricing)
class InternshipPricingAdmin(admin.ModelAdmin):
    list_display = ('duration', 'price', 'is_active')
    list_editable = ('price', 'is_active')
    search_fields = ('duration',)


# ===========================================================
# Daily Challenger Admin (New System)
# ===========================================================
@admin.register(ChallengeTrack)
class ChallengeTrackAdmin(admin.ModelAdmin):
    list_display  = ('emoji', 'name', 'is_system', 'created_by', 'description')
    list_filter   = ('is_system',)
    search_fields = ('name', 'description')
    list_editable = ('is_system',)


@admin.register(UserChallengeEnrollment)
class UserChallengeEnrollmentAdmin(admin.ModelAdmin):
    list_display  = ('user', 'track', 'target_days', 'enrolled_at', 'is_active')
    list_filter   = ('target_days', 'is_active', 'track')
    search_fields = ('user__username', 'track__name')
    list_editable = ('is_active',)


@admin.register(DailyTrackCheckIn)
class DailyTrackCheckInAdmin(admin.ModelAdmin):
    list_display  = ('user', 'track', 'date', 'notes', 'done_at')
    list_filter   = ('track', 'date')
    search_fields = ('user__username', 'track__name', 'notes')
    date_hierarchy = 'date'


@admin.register(MilestoneAchievement)
class MilestoneAchievementAdmin(admin.ModelAdmin):
    list_display  = ('user', 'track', 'milestone_days', 'achieved_at', 'reward_sent')
    list_filter   = ('milestone_days', 'reward_sent', 'track')
    list_editable = ('reward_sent',)
    search_fields = ('user__username', 'track__name')


@admin.register(UserStreak)
class UserStreakAdmin(admin.ModelAdmin):
    list_display  = ('user', 'current_streak', 'longest_streak', 'last_completion_date')
    search_fields = ('user__username',)
    ordering      = ('-current_streak',)


# ===========================================================
# Client System Admin
# ===========================================================
class ClientProjectMilestoneInline(admin.TabularInline):
    model = ClientProjectMilestone
    extra = 1
    fields = ('title', 'description', 'due_date', 'is_completed', 'completed_at', 'order')

class ClientProjectDeliverableInline(admin.TabularInline):
    model = ClientProjectDeliverable
    extra = 1
    fields = ('title', 'file', 'description')

class ClientProjectUpdateInline(admin.StackedInline):
    model = ClientProjectUpdate
    extra = 1
    fields = ('message', 'posted_by')

class ClientInvoiceInline(admin.TabularInline):
    model = ClientInvoice
    extra = 0
    fields = ('invoice_number', 'amount', 'status', 'description', 'due_date', 'paid_date', 'transaction_id')


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'phone', 'industry', 'created_at')
    search_fields = ('company_name', 'user__email', 'phone')
    list_filter = ('industry',)
    readonly_fields = ('created_at',)


@admin.register(ClientProject)
class ClientProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'service_type', 'status', 'progress', 'start_date', 'deadline')
    list_filter = ('status', 'service_type')
    search_fields = ('title', 'client__company_name')
    list_editable = ('status', 'progress')
    inlines = [ClientProjectMilestoneInline, ClientProjectDeliverableInline, ClientProjectUpdateInline, ClientInvoiceInline]


@admin.register(ClientInvoice)
class ClientInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'project', 'amount', 'status', 'issued_date', 'due_date', 'paid_date')
    list_filter = ('status',)
    search_fields = ('invoice_number', 'project__title', 'project__client__company_name')
    list_editable = ('status',)


# ===========================================================
# Email Template Admin
# Only admin-staff can edit; templates cannot be deleted.
# ===========================================================
@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display  = ('label', 'name', 'short_subject', 'updated_at')
    readonly_fields = ('name', 'updated_at', 'placeholder_reference')
    fields = ('name', 'label', 'subject', 'placeholder_reference', 'body', 'updated_at')

    def short_subject(self, obj):
        return obj.subject[:80] + '…' if len(obj.subject) > 80 else obj.subject
    short_subject.short_description = 'Subject'

    def placeholder_reference(self, obj):
        """Shows the available {placeholder} variables directly in the change form."""
        if obj.name == 'offer_letter':
            ref = OFFER_LETTER_PLACEHOLDERS
        else:
            ref = CREDENTIALS_PLACEHOLDERS
        return format_html(
            '<div style="background:#f8f9fa;border:1px solid #dee2e6;border-radius:6px;'
            'padding:12px 16px;font-family:monospace;white-space:pre-wrap;'
            'font-size:0.85em;color:#212529;">{}\n</div>',
            ref
        )
    placeholder_reference.short_description = '📋 Available Placeholders'

    # Prevent admins from accidentally deleting the seeded templates
    def has_delete_permission(self, request, obj=None):
        return False

    # Prevent adding new templates beyond the two seeded ones
    def has_add_permission(self, request):
        return EmailTemplate.objects.count() < len(EmailTemplate.TEMPLATE_CHOICES)


# ===========================================================
# Review Admin — approve/reject public reviews from admin
# ===========================================================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('name', 'role', 'star_display', 'is_approved', 'created_at', 'short_message')
    list_filter   = ('is_approved', 'rating')
    search_fields = ('name', 'role', 'message')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def star_display(self, obj):
        filled = '★' * obj.rating
        empty  = '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color:#f59e0b;font-size:1.1em;">{}</span>'
            '<span style="color:#d1d5db;">{}</span>',
            filled, empty
        )
    star_display.short_description = 'Rating'

    def short_message(self, obj):
        return obj.message[:60] + '…' if len(obj.message) > 60 else obj.message
    short_message.short_description = 'Message'

