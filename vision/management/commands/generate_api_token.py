"""
management/commands/generate_api_token.py

Creates (or retrieves) a DRF Token for an admin user.

Usage:
  python manage.py generate_api_token --username admin
  python manage.py generate_api_token --username admin --reset
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = "Generate (or retrieve) a DRF API Token for an admin user."

    def add_arguments(self, parser):
        parser.add_argument(
            '--username', type=str, required=True,
            help="Django username of the staff/superuser"
        )
        parser.add_argument(
            '--reset', action='store_true',
            help="Delete existing token and create a fresh one"
        )

    def handle(self, *args, **options):
        username = options['username']
        reset    = options['reset']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"User '{username}' does not exist.")

        if not user.is_staff:
            raise CommandError(
                f"User '{username}' is not a staff member. "
                "Grant staff access first (python manage.py shell → user.is_staff = True; user.save())"
            )

        if reset:
            Token.objects.filter(user=user).delete()
            self.stdout.write(self.style.WARNING("Existing token deleted."))

        token, created = Token.objects.get_or_create(user=user)

        status = "Created" if created else "Existing"
        self.stdout.write(self.style.SUCCESS(
            f"\n{'='*60}\n"
            f"  {status} API Token for '{username}'\n"
            f"{'='*60}\n"
            f"  Token: {token.key}\n"
            f"{'='*60}\n\n"
            "Use this token in Power BI / Postman as:\n"
            "  Header Name:  Authorization\n"
            f"  Header Value: Token {token.key}\n"
        ))
