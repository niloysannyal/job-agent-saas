import logging
import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings

logger = logging.getLogger(__name__)


def is_smtp_configured() -> bool:
    """Check if outbound SMTP server credentials are fully configured."""
    return bool(settings.SMTP_HOST and settings.SMTP_USER)


def generate_otp() -> str:
    """Generate a cryptographically secure 6-digit numeric OTP code."""
    # 000000 - 999999
    code = secrets.randbelow(1_000_000)
    return f"{code:06d}"


def send_otp_email(to_email: str, otp_code: str) -> bool:
    """
    Send 6-digit OTP verification email to user.
    Falls back gracefully to secure development logging if SMTP is not configured.
    """
    if not is_smtp_configured():
        logger.info(
            f"[JobEazy Auth Dev Mode] OTP code generated for {to_email}: {otp_code} "
            f"(Valid for {settings.OTP_EXPIRE_MINUTES} minutes)"
        )
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"{otp_code} is your JobEazy verification code"
        msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
        msg["To"] = to_email

        plain_text = f"""
Welcome to JobEazy!

Your verification code is: {otp_code}

This code will expire in {settings.OTP_EXPIRE_MINUTES} minutes. If you did not request this, please disregard this email.

Best regards,
The JobEazy Team
https://jobeazy.ai
"""

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>JobEazy Verification Code</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0b0f17; color: #e2e8f0; margin: 0; padding: 40px 20px;">
  <div style="max-width: 500px; margin: 0 auto; background-color: #131b26; border: 1px solid #1e293b; border-radius: 12px; padding: 32px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
    <div style="text-align: center; margin-bottom: 24px;">
      <h2 style="color: #00e599; margin: 0; font-size: 24px; letter-spacing: -0.5px;">JobEazy</h2>
      <p style="color: #94a3b8; font-size: 13px; margin: 4px 0 0 0;">Autonomous Job Application SaaS</p>
    </div>
    
    <h3 style="color: #f8fafc; font-size: 18px; margin-bottom: 8px;">Confirm Your Email Address</h3>
    <p style="color: #94a3b8; font-size: 14px; line-height: 1.5; margin: 0 0 20px 0;">
      Use the 6-digit verification code below to complete your JobEazy account registration:
    </p>

    <div style="background-color: #0d131f; border: 1px solid #22c55e44; border-radius: 8px; padding: 18px; text-align: center; margin: 24px 0;">
      <span style="font-size: 32px; font-weight: 700; letter-spacing: 6px; color: #00e599; font-family: monospace;">{otp_code}</span>
    </div>

    <p style="color: #64748b; font-size: 12px; line-height: 1.5; margin: 20px 0 0 0;">
      ⏱️ This code is valid for <strong>{settings.OTP_EXPIRE_MINUTES} minutes</strong> and can only be used once.<br>
      If you did not request this verification code, you can safely ignore this email.
    </p>

    <div style="border-top: 1px solid #1e293b; margin-top: 28px; padding-top: 16px; text-align: center;">
      <p style="color: #475569; font-size: 11px; margin: 0;">
        &copy; 2026 JobEazy. All rights reserved. • Built for high-leverage job search automation.
      </p>
    </div>
  </div>
</body>
</html>
"""

        msg.attach(MIMEText(plain_text, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        if settings.SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10)
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10)
            if settings.SMTP_TLS:
                server.starttls()

        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        server.send_message(msg)
        server.quit()
        logger.info(f"Verification email successfully sent to {to_email}")
        return True
    except Exception as exc:
        logger.error(f"Failed to send verification email to {to_email}: {exc}", exc_info=True)
        return False

