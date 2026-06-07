# Hostinger Email Setup Instructions

## Step 1: Create Email Account in Hostinger

1. Log in to your Hostinger account at https://hpanel.hostinger.com
2. Go to **Emails** section
3. Click **Create Email Account**
4. Create an email like: `noreply@trhvision.in` or `support@trhvision.in`
5. Set a strong password
6. Save the email and password

## Step 2: Update Django Settings

Open `TRH/settings.py` and update these lines:

```python
EMAIL_HOST_USER = 'noreply@trhvision.in'  # Your created email
EMAIL_HOST_PASSWORD = 'your_actual_password'  # The password you set
```

## Step 3: Test the Configuration

### Option A: Test with Console (Development Mode)

1. In `settings.py`, temporarily comment out the SMTP backend:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   ```

2. Restart your Django server
3. Go to http://localhost:8000/sigin/
4. Click "Forgot?" link
5. Enter a test email
6. Check your terminal - you should see the email content printed

### Option B: Test with Real Email (Production Mode)

1. Make sure `settings.py` has:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   ```

2. Restart your Django server
3. Go to http://localhost:8000/sigin/
4. Click "Forgot?" link
5. Enter your actual email address (must be a user in your database)
6. Check your email inbox
7. Click the reset link
8. Set a new password

## Troubleshooting

### "SMTPAuthenticationError"
- Double-check your email and password in `settings.py`
- Make sure the email account exists in Hostinger
- Try logging into the email via webmail to verify credentials

### "Connection refused" or "Timeout"
- Check if your firewall is blocking port 587
- Try using port 465 with `EMAIL_USE_SSL = True` instead of `EMAIL_USE_TLS`

### Email not received
- Check spam/junk folder
- Verify the user's email exists in your database
- Check Django server logs for errors

## Security Best Practices

For production deployment, use environment variables instead of hardcoding passwords:

```python
import os

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'noreply@trhvision.in')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

Then set these in your production environment.
