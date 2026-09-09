import httpx
from app.core.config import get_settings

settings = get_settings()

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


async def _send_email(to_email: str, subject: str, text_content: str, html_content: str | None = None) -> None:
    headers = {
        "api-key": settings.BREVO_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "sender": {"name": settings.BREVO_SENDER_NAME, "email": settings.BREVO_SENDER_EMAIL},
        "to": [{"email": to_email}],
        "subject": subject,
        "textContent": text_content,
    }
    if html_content:
        payload["htmlContent"] = html_content

    async with httpx.AsyncClient() as client:
        response = await client.post(BREVO_API_URL, json=payload, headers=headers, timeout=10.0)
        response.raise_for_status()


def _email_shell(header_label: str, body_html: str) -> str:
    """Shared card wrapper so every email looks consistent."""
    return f"""
    <html>
    <body style="margin:0;padding:0;background:#EEF1EC;font-family:Arial,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background:#EEF1EC;padding:32px 0;">
        <tr>
          <td align="center">
            <table width="480" cellpadding="0" cellspacing="0" style="background:#FFFFFF;border-radius:12px;overflow:hidden;border:1px solid #C9D2C4;">
              <tr>
                <td style="background:#3F6B4F;padding:24px 32px;">
                  <div style="color:#FFFFFF;font-family:Georgia,serif;font-size:20px;font-weight:700;">Field Log</div>
                  <div style="color:#DDEDD9;font-size:12px;letter-spacing:0.06em;text-transform:uppercase;margin-top:2px;">{header_label}</div>
                </td>
              </tr>
              <tr>
                <td style="padding:32px;">
                  {body_html}
                </td>
              </tr>
              <tr>
                <td style="padding:16px 32px;background:#F5F7F3;border-top:1px solid #C9D2C4;">
                  <div style="font-size:12px;color:#4B5A50;font-family:Arial,sans-serif;">
                    If you didn't request this, you can safely ignore this email.
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """


async def send_otp_email(email: str, code: str, purpose: str) -> None:
    text = f"Your verification code is: {code}\n\nUse this code to {purpose}. It will expire shortly."

    body = f"""
      <div style="font-size:15px;color:#16241B;font-family:Arial,sans-serif;margin-bottom:8px;">
        Here's your verification code.
      </div>
      <div style="font-size:14px;color:#4B5A50;font-family:Arial,sans-serif;margin-bottom:24px;">
        Use this code to {purpose}. It expires shortly, so enter it soon.
      </div>
      <table width="100%" cellpadding="0" cellspacing="0" style="background:#F5F7F3;border:1px solid #C9D2C4;border-radius:8px;">
        <tr>
          <td style="padding:20px;text-align:center;">
            <div style="font-family:'Courier New',monospace;font-size:32px;font-weight:700;letter-spacing:8px;color:#3F6B4F;">
              {code}
            </div>
          </td>
        </tr>
      </table>
    """
    html = _email_shell("Email Verification", body)
    await _send_email(email, "Your Student Progress Tracker verification code", text, html)


async def send_password_reset_email(email: str, reset_link: str) -> None:
    text = (
        f"We received a request to reset your password.\n\n"
        f"Click the link below to set a new password:\n{reset_link}\n\n"
        f"This link expires in 15 minutes. If you didn't request this, ignore this email."
    )

    body = f"""
      <div style="font-size:15px;color:#16241B;font-family:Arial,sans-serif;margin-bottom:8px;">
        Password reset requested.
      </div>
      <div style="font-size:14px;color:#4B5A50;font-family:Arial,sans-serif;margin-bottom:24px;">
        Click the button below to set a new password. This link expires in 15 minutes.
      </div>
      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td align="center">
            <a href="{reset_link}" style="display:inline-block;background:#3F6B4F;color:#FFFFFF;text-decoration:none;
               font-family:Arial,sans-serif;font-size:15px;font-weight:600;padding:14px 32px;border-radius:8px;">
              Reset Password
            </a>
          </td>
        </tr>
      </table>
      <div style="font-size:12px;color:#4B5A50;font-family:Arial,sans-serif;margin-top:20px;word-break:break-all;">
        Or copy this link: {reset_link}
      </div>
    """
    html = _email_shell("Password Reset", body)
    await _send_email(email, "Reset your Student Progress Tracker password", text, html)


async def send_digest_email(email: str, name: str, text_content: str, html_content: str) -> None:
    await _send_email(email, "Your weekly study summary", text_content, html_content)

async def send_password_changed_email(email: str, name: str) -> None:
    text = (
        f"Hi {name},\n\n"
        f"This is a confirmation that your Student Progress Tracker password was just changed.\n\n"
        f"If you didn't make this change, please reset your password immediately or contact support."
    )

    body = f"""
      <div style="font-size:15px;color:#16241B;font-family:Arial,sans-serif;margin-bottom:8px;">
        Hi {name}, your password was changed.
      </div>
      <div style="font-size:14px;color:#4B5A50;font-family:Arial,sans-serif;margin-bottom:24px;">
        This is a confirmation that your password was just updated. If this wasn't you, reset your password
        immediately or contact support right away.
      </div>
    """
    html = _email_shell("Password Changed", body)
    await _send_email(email, "Your Student Progress Tracker password was changed", text, html)

async def send_account_deactivated_email(email: str, name: str) -> None:
    text = (
        f"Hi {name},\n\n"
        f"This is a confirmation that your Student Progress Tracker account has been deactivated.\n\n"
        f"If you didn't request this, please contact support right away."
    )

    body = f"""
      <div style="font-size:15px;color:#16241B;font-family:Arial,sans-serif;margin-bottom:8px;">
        Hi {name}, your account has been deactivated.
      </div>
      <div style="font-size:14px;color:#4B5A50;font-family:Arial,sans-serif;margin-bottom:24px;">
        This is a confirmation that your account was just deactivated. You won't be able to log in until it's
        reactivated. If this wasn't you, please contact support immediately.
      </div>
    """
    html = _email_shell("Account Deactivated", body)
    await _send_email(email, "Your Student Progress Tracker account was deactivated", text, html)


async def send_account_deleted_email(email: str, name: str) -> None:
    text = (
        f"Hi {name},\n\n"
        f"This is a confirmation that your Student Progress Tracker account and all associated data "
        f"have been permanently deleted.\n\n"
        f"If you didn't request this, please contact support right away."
    )

    body = f"""
      <div style="font-size:15px;color:#16241B;font-family:Arial,sans-serif;margin-bottom:8px;">
        Hi {name}, your account has been deleted.
      </div>
      <div style="font-size:14px;color:#4B5A50;font-family:Arial,sans-serif;margin-bottom:24px;">
        This is a confirmation that your account and all associated data have been permanently deleted.
        This can't be undone. If this wasn't you, please contact support immediately.
      </div>
    """
    html = _email_shell("Account Deleted", body)
    await _send_email(email, "Your Student Progress Tracker account was deleted", text, html)