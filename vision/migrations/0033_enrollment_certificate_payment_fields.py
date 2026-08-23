from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vision', '0032_emailtemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='certificate_paid',
            field=models.BooleanField(
                default=False,
                help_text='True when the student has paid for the completion certificate'
            ),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='certificate_payment_amount',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Amount paid by the student to receive their completion certificate',
                max_digits=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='certificate_payment_id',
            field=models.CharField(
                blank=True,
                help_text='Razorpay/UPI payment ID for the certificate payment',
                max_length=200,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='certificate_payment_date',
            field=models.DateTimeField(
                blank=True,
                help_text='When the student completed the certificate payment',
                null=True,
            ),
        ),
    ]
