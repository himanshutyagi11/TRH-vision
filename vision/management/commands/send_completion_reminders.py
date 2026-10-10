"""
Management command: send_completion_reminders
=============================================
Finds all approved, active enrollments whose internship END DATE falls
exactly 5, 6 or 7 days from today and sends a reminder email.

Run once per day via server cron:
    python manage.py send_completion_reminders

Or from the admin Mail Centre with a POST button.
"""
import datetime
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone


class Command(BaseCommand):
    help = "Send internship-completion reminder emails to students finishing in 5-7 days."

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Print matching students without sending emails.",
        )
        parser.add_argument(
            '--days-before',
            type=int,
            default=None,
            help="Override the window (comma-separated not supported; pass once per value). "
                 "Defaults to 5, 6, and 7 days before end date.",
        )

    def handle(self, *args, **options):
        from vision.models import Enrollment, EmailTemplate, Profile

        dry_run = options['dry_run']
        today = timezone.localdate()

        # Build list of days before completion to target
        if options['days_before'] is not None:
            target_windows = [options['days_before']]
        else:
            target_windows = [5, 6, 7]

        # Duration string → integer months mapping
        duration_map = {
            '1 Month': 1,
            '2 Months': 2,
            '3 Months': 3,
            '6 Months': 6,
        }

        # Load the email template (admin-editable)
        tpl = EmailTemplate.objects.filter(name='internship_completion').first()

        sent_count = 0
        skipped_count = 0

        # Only look at approved enrollments that have a start_date set
        enrollments = Enrollment.objects.filter(
            is_approved=True,
            start_date__isnull=False,
            completion_reminder_sent=False,
        )

        for enrollment in enrollments:
            months = duration_map.get(enrollment.duration, 1)
            # Compute end date: start_date + N months
            start = enrollment.start_date
            try:
                end_date = start.replace(month=start.month + months)
            except ValueError:
                # Month overflow (e.g. Jan 31 + 1 month → Feb 31 doesn't exist)
                import calendar
                end_month = (start.month + months - 1) % 12 + 1
                end_year = start.year + (start.month + months - 1) // 12
                end_day = min(start.day, calendar.monthrange(end_year, end_month)[1])
                end_date = datetime.date(end_year, end_month, end_day)

            days_remaining = (end_date - today).days

            if days_remaining not in target_windows:
                continue

            # Get student_id if available
            student_id = ''
            try:
                profile = enrollment.user_set.first().profile if hasattr(enrollment, 'user_set') else None
            except Exception:
                profile = None
            # Try via the linked User (email matches)
            if not profile:
                from django.contrib.auth.models import User
                user = User.objects.filter(email=enrollment.email).first()
                if user:
                    try:
                        profile = user.profile
                        student_id = profile.student_id
                    except Exception:
                        student_id = ''

            template_ctx = {
                'name':       enrollment.name,
                'domain':     enrollment.domain,
                'duration':   enrollment.duration,
                'email':      enrollment.email,
                'student_id': student_id,
                'start_date': start.strftime('%B %d, %Y'),
                'end_date':   end_date.strftime('%B %d, %Y'),
                'days_left':  str(days_remaining),
            }

            if tpl:
                subject, body = tpl.get_rendered(template_ctx)
            else:
                # Hardcoded fallback
                subject = (
                    f"\U0001f393 Your {enrollment.domain} Internship is Ending Soon — TRHvision"
                )
                body = (
                    f"Dear {enrollment.name},\n\n"
                    f"We hope your internship journey with TRHvision has been a rewarding experience!\n\n"
                    f"This is a friendly reminder that your {enrollment.domain} internship "
                    f"({enrollment.duration}) is scheduled to end on "
                    f"{end_date.strftime('%B %d, %Y')} — just {days_remaining} day(s) from now.\n\n"
                    "Please make sure you have:\n"
                    "  \u2714\ufe0f  Completed all your assigned tasks\n"
                    "  \u2714\ufe0f  Submitted your final project\n"
                    "  \u2714\ufe0f  Finished your learning modules\n\n"
                    "Once you've completed everything, you can apply for your internship completion certificate through the portal.\n\n"
                    "Best regards,\n"
                    "TRHvision Academy Team\n"
                    "\U0001f4e7 info@trhvision.in | \U0001f310 www.trhvision.in"
                )

            if dry_run:
                self.stdout.write(
                    self.style.WARNING(
                        f"[DRY-RUN] Would send to {enrollment.name} <{enrollment.email}> "
                        f"(ends {end_date}, {days_remaining}d left)"
                    )
                )
                sent_count += 1
                continue

            try:
                from_email = (
                    getattr(settings, 'EMAIL_HOST_USER', None)
                    or getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@trhvision.in')
                )
                msg = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=from_email,
                    to=[enrollment.email],
                )
                msg.send(fail_silently=False)

                enrollment.completion_reminder_sent = True
                enrollment.save(update_fields=['completion_reminder_sent'])

                self.stdout.write(
                    self.style.SUCCESS(
                        f"  \u2713 Sent to {enrollment.name} <{enrollment.email}> "
                        f"(ends {end_date}, {days_remaining}d left)"
                    )
                )
                sent_count += 1

            except Exception as exc:
                self.stdout.write(
                    self.style.ERROR(
                        f"  \u2717 Failed for {enrollment.name} <{enrollment.email}>: {exc}"
                    )
                )
                skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. Sent: {sent_count} | Failed: {skipped_count}"
            )
        )
