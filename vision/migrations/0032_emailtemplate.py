from django.db import migrations, models


OFFER_LETTER_SUBJECT = (
    "\U0001f389 Internship Offer Letter \u2013 {domain} | TRHvision Academy"
)

OFFER_LETTER_BODY = """\
Dear {name},

Greetings from TRHvision Academy! \U0001f389

We are delighted to officially welcome you to our internship programme. It gives us great pleasure to inform you that your enrollment in the {domain} internship programme for a duration of {duration} has been reviewed and approved by our academic team.

Please find your official Internship Offer Letter attached to this email. This document confirms your selection and outlines the terms of your internship.

We encourage you to carefully read through the offer letter and reach out to us should you have any questions or require clarification.

Your internship journey begins on {start_date}. We will soon send you your portal login credentials so you can begin accessing your learning materials and track your progress.

We look forward to a productive and enriching learning experience with you!

With warm regards,
TRHvision Academy Team
\U0001f4e7 info@trhvision.in | \U0001f310 www.trhvision.in"""

CREDENTIALS_SUBJECT = (
    "\U0001f511 Your TRHvision Academy Login Credentials \u2013 {domain} Internship"
)

CREDENTIALS_BODY = """\
Dear {name},

We hope you have received your Offer Letter and are excited to begin your internship at TRHvision Academy!

Your student account on the TRHvision Academy Portal is now active. Please use the credentials below to log in to your personalised student dashboard where you can access learning materials, track your milestones, and submit your tasks and projects.

\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501
\U0001f393 Your Login Credentials
\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501
  Portal URL : {portal_url}
  Student ID : {student_id}
  Username   : {email}
  Password   : {password}
\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501

\U0001f4cc Important Notes:
  \u2022 Please log in immediately and change your password for security.
  \u2022 Complete your profile setup once you log in.
  \u2022 Follow the module guidelines sequentially for best results.
  \u2022 Your offer letter is also available for download from your dashboard.

If you face any issues logging in, please reply to this email or contact us at info@trhvision.in.

We wish you a wonderful and productive internship experience!

Warm regards,
TRHvision Academy Team
\U0001f4e7 info@trhvision.in | \U0001f310 www.trhvision.in"""


def seed_email_templates(apps, schema_editor):
    EmailTemplate = apps.get_model('vision', 'EmailTemplate')
    EmailTemplate.objects.get_or_create(
        name='offer_letter',
        defaults={
            'label': 'Offer Letter Email',
            'subject': OFFER_LETTER_SUBJECT,
            'body': OFFER_LETTER_BODY,
        }
    )
    EmailTemplate.objects.get_or_create(
        name='login_credentials',
        defaults={
            'label': 'Login Credentials Email',
            'subject': CREDENTIALS_SUBJECT,
            'body': CREDENTIALS_BODY,
        }
    )


def unseed_email_templates(apps, schema_editor):
    EmailTemplate = apps.get_model('vision', 'EmailTemplate')
    EmailTemplate.objects.filter(name__in=['offer_letter', 'login_credentials']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('vision', '0031_enrollment_offer_letter_sent_enrollment_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(
                    choices=[('offer_letter', '\U0001f4c4 Offer Letter Email'), ('login_credentials', '\U0001f511 Login Credentials Email')],
                    help_text='Internal identifier. Do not change.',
                    max_length=50,
                    unique=True,
                )),
                ('label', models.CharField(help_text='Friendly name shown in admin.', max_length=200)),
                ('subject', models.CharField(
                    help_text='Email subject line. Use {name}, {domain}, {duration} as placeholders.',
                    max_length=500,
                )),
                ('body', models.TextField(
                    help_text='Email body text. See the placeholder reference below for available variables.',
                )),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Email Template',
                'verbose_name_plural': '\U0001f4e7 Email Templates',
            },
        ),
        migrations.RunPython(seed_email_templates, reverse_code=unseed_email_templates),
    ]
