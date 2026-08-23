from django.apps import AppConfig
import os
import sys


def _record_student_attendance(sender, request, user, **kwargs):
    """
    Signal handler for django.contrib.auth.signals.user_logged_in.
    Records one attendance row per student per calendar day.
    Skips staff, superusers, and client-portal accounts.
    """
    # Only track regular student accounts
    if user.is_staff or user.is_superuser:
        return
    # Skip client portal users
    if hasattr(user, 'client_profile'):
        return
    # Skip if the user has no student profile
    if not hasattr(user, 'profile'):
        return

    try:
        from django.utils import timezone
        from django.db.models import F
        from .models import StudentAttendance

        today = timezone.localdate()
        now   = timezone.now()

        # Get client IP
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
        ip = x_forwarded.split(',')[0].strip() if x_forwarded else request.META.get('REMOTE_ADDR', '')
        ua = request.META.get('HTTP_USER_AGENT', '')[:500]

        record, created = StudentAttendance.objects.get_or_create(
            user=user,
            date=today,
            defaults={
                'login_time': now,
                'ip_address': ip or None,
                'user_agent': ua,
                'login_count': 1,
            }
        )
        if not created:
            # Already logged in today — just increment the counter
            StudentAttendance.objects.filter(pk=record.pk).update(
                login_count=F('login_count') + 1
            )
    except Exception:
        pass  # Never break the login flow


class VisionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vision'

    def ready(self):
        # Connect the attendance signal
        from django.contrib.auth.signals import user_logged_in
        user_logged_in.connect(_record_student_attendance, dispatch_uid='vision_student_attendance')
        # NOTE: Auto-dispatcher disabled — admin now uses the manual one-click
        # "Send Offer Letter" → "Send Credentials" flow in the enrollments panel.
        # To re-enable, uncomment the block below.
        # is_runserver = 'runserver' in sys.argv
        # if not is_runserver or os.environ.get('RUN_MAIN') == 'true':
        #     from .views import start_approved_enrollments_dispatcher
        #     start_approved_enrollments_dispatcher()
        
        # Correct email template placeholders in DB
        try:
            from .models import EmailTemplate, Enrollment, Profile
            tpl = EmailTemplate.objects.filter(name='login_credentials').first()
            if tpl:
                modified = False
                
                # Check for incorrect placeholders
                if 'Student ID : {name}' in tpl.body:
                    tpl.body = tpl.body.replace('Student ID : {name}', 'Student ID : {student_id}')
                    modified = True
                elif '{student_id}' not in tpl.body:
                    import re
                    new_body = re.sub(r'Student\s+ID\s*:\s*\{name\}', 'Student ID : {student_id}', tpl.body, flags=re.IGNORECASE)
                    if new_body != tpl.body:
                        tpl.body = new_body
                        modified = True
                
                if modified:
                    tpl.save()

                # Correct database profiles with incorrect student ID formats (e.g. name or blank or no TRH prefix)
                from .views import _generate_unid
                for p in Profile.objects.all():
                    is_invalid = False
                    if not p.student_id:
                        is_invalid = True
                    elif ' ' in p.student_id or '@' in p.student_id:
                        is_invalid = True
                    elif not p.student_id.startswith('TRH'):
                        is_invalid = True
                    
                    if is_invalid:
                        e = Enrollment.objects.filter(email=p.user.email).first()
                        if e:
                            p.student_id = _generate_unid(e)
                        else:
                            p.student_id = f"TRH20-26-{p.user.id:03d}"
                        p.save()
        except Exception:
            pass

