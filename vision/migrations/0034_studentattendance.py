from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vision', '0033_enrollment_certificate_payment_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='Calendar date of the login')),
                ('login_time', models.DateTimeField(help_text='Timestamp of the first login on this date')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.CharField(blank=True, max_length=500)),
                ('login_count', models.PositiveIntegerField(
                    default=1,
                    help_text='How many times the student logged in on this date'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='attendance_records',
                    to='auth.user',
                )),
            ],
            options={
                'verbose_name': 'Student Attendance',
                'verbose_name_plural': 'Student Attendance',
                'ordering': ['-date', 'user'],
                'unique_together': {('user', 'date')},
            },
        ),
    ]
