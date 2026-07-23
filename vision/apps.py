from django.apps import AppConfig
import os
import sys

class VisionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vision'

    def ready(self):
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

