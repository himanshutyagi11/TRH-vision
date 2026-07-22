"""
Quick SMTP diagnostic test — run this DIRECTLY in terminal:
    python test_smtp.py
"""
import smtplib
import ssl
from email.mime.text import MIMEText

# ── Edit these if needed ───────────────────────────────────────────
EMAIL_USER     = "contact@trhvision.in"
EMAIL_PASSWORD = "AiKqmt@2443"
EMAIL_TO       = "contact@trhvision.in"   # send test to yourself
# ──────────────────────────────────────────────────────────────────

def send_test_msg(smtp_obj, port_label):
    msg = MIMEText(f"SMTP test from Django app - Port {port_label} works!", "plain", "utf-8")
    msg["Subject"] = "TRHvision SMTP Test"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    smtp_obj.sendmail(EMAIL_USER, [EMAIL_TO], msg.as_string())

def test_port_465():
    print("\n[TEST 1] Trying smtp.hostinger.com:465 (SSL)...")
    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.hostinger.com", 465, context=ctx, timeout=10) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            send_test_msg(smtp, "465 SSL")
        print("  ✅ PORT 465 SSL — SUCCESS! Email sent.")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"  ❌ AUTH FAILED on 465: {e}")
    except Exception as e:
        print(f"  ❌ ERROR on 465: {e}")
    return False

def test_port_587():
    print("\n[TEST 2] Trying smtp.hostinger.com:587 (STARTTLS)...")
    try:
        with smtplib.SMTP("smtp.hostinger.com", 587, timeout=10) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            send_test_msg(smtp, "587 TLS")
        print("  ✅ PORT 587 TLS — SUCCESS! Email sent.")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"  ❌ AUTH FAILED on 587: {e}")
    except Exception as e:
        print(f"  ❌ ERROR on 587: {e}")
    return False

if __name__ == "__main__":
    print("=" * 55)
    print("  TRHvision SMTP Diagnostic")
    print(f"  User: {EMAIL_USER}")
    print("=" * 55)

    ok465 = test_port_465()
    ok587 = test_port_587()

    print("\n" + "=" * 55)
    if ok465:
        print("✅ Use PORT 465 with SSL in settings.py")
    elif ok587:
        print("✅ Use PORT 587 with TLS in settings.py")
    else:
        print("❌ Authentication or Connection Failed.")
    print("=" * 55)