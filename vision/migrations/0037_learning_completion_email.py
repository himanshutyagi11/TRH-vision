from django.db import migrations, models


COMPLETION_SUBJECT = (
    "\U0001f393 Congratulations! You've Completed Your Learning Content"
    " \u2013 {domain} | TRHvision Academy"
)

COMPLETION_BODY = """\
Dear {name},

Congratulations on a fantastic achievement! \U0001f389

We are thrilled to inform you that you have successfully completed all {total} lessons of the \
{domain} learning content on the TRHvision Academy portal.

This milestone reflects your commitment, hard work, and passion for learning. \
We are incredibly proud of your progress throughout the internship programme.

\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501
\U0001f4cb Your Completion Summary
\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501
  Student Name  : {name}
  Student ID    : {student_id}
  Domain        : {domain}
  Duration      : {duration}
  Lessons Done  : {total}
\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501

\U0001f4cc What Happens Next?
  \u2022 Continue completing your tasks and assignments on the portal.
  \u2022 Submit your final project for review by the academic team.
  \u2022 Once your project is approved, you will be eligible to receive your Completion Certificate.
  \u2022 Reach out to us at info@trhvision.in if you have any questions.

Keep up the great work and finish strong! We look forward to presenting you with your \
completion certificate very soon.

With warm regards,
TRHvision Academy Team
\U0001f4e7 info@trhvision.in | \U0001f310 www.trhvision.in"""


def seed_completion_template(apps, schema_editor):
    EmailTemplate = apps.get_model('vision', 'EmailTemplate')
    EmailTemplate.objects.get_or_create(
        name='learning_completion',
        defaults={
            'label': 'Learning Content Completion Email',
            'subject': COMPLETION_SUBJECT,
            'body': COMPLETION_BODY,
        }
    )


def unseed_completion_template(apps, schema_editor):
    EmailTemplate = apps.get_model('vision', 'EmailTemplate')
    EmailTemplate.objects.filter(name='learning_completion').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('vision', '0036_learning_hub'),
    ]

    operations = [
        # 1. Add the new boolean field to Enrollment
        migrations.AddField(
            model_name='enrollment',
            name='learning_completion_email_sent',
            field=models.BooleanField(
                default=False,
                help_text='Set to True after the learning-completion congratulations email has been sent to this student',
            ),
        ),
        # 2. Alter the TEMPLATE_CHOICES on EmailTemplate (no schema change needed,
        #    choices are validated in Python only — but we record it for consistency)
        migrations.AlterField(
            model_name='emailtemplate',
            name='name',
            field=models.CharField(
                choices=[
                    ('offer_letter', 'Offer Letter Email'),
                    ('login_credentials', 'Login Credentials Email'),
                    ('learning_completion', 'Learning Content Completion Email'),
                ],
                help_text='Internal identifier. Do not change.',
                max_length=50,
                unique=True,
            ),
        ),
        # 3. Seed the new template row
        migrations.RunPython(seed_completion_template, reverse_code=unseed_completion_template),
    ]
