"""
Quick SMTP diagnostic test — run this DIRECTLY in terminal:
  python test_smtp.py

This bypasses Django entirely and tests Hostinger SMTP raw.
"""
import smtplib
import ssl

# ── Edit these if needed ───────────────────────────────────────────
EMAIL_USER     = "contact@trhvision.in"
EMAIL_PASSWORD = "AiKqmt@2443"
EMAIL_TO       = "contact@trhvision.in"   # send test to yourself
# ──────────────────────────────────────────────────────────────────

def test_port_465():
    print("\n[TEST 1] Trying smtp.hostinger.com:465 (SSL)...")
    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.hostinger.com", 465, context=ctx, timeout=10) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_USER, EMAIL_TO,
                          "Subject: TRHvision SMTP Test\n\nSMTP test from Django app — Port 465 SSL works!")
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
            smtp.sendmail(EMAIL_USER, EMAIL_TO,
                          "Subject: TRHvision SMTP Test\n\nSMTP test from Django app — Port 587 TLS works!")
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
    print(f"  Pass: {'*' * (len(EMAIL_PASSWORD)-3)}{EMAIL_PASSWORD[-3:]}")
    print("=" * 55)

    ok465 = test_port_465()
    ok587 = test_port_587()

    print("\n" + "=" * 55)
    if ok465:
        print("✅ Use PORT 465 with SSL in settings.py (already set!)")
    elif ok587:
        print("✅ Use PORT 587 with TLS in settings.py")
        print("   Change settings: EMAIL_PORT=587, EMAIL_USE_TLS=True, EMAIL_USE_SSL=False")
    else:
        print("❌ Both ports failed. The password is wrong.")
        print("   → Log into Hostinger hPanel > Emails > Email Accounts")
        print("   → Find contact@trhvision.in and reset the password")
        print("   → Update .env with the new password and restart server")
    print("=" * 55)
