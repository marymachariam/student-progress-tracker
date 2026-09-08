import httpx
from app.core.config import get_settings

settings = get_settings()

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


async def _send_email(to_email: str, subject: str, text_content: str) -> None:
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

    async with httpx.AsyncClient() as client:
        response = await client.post(BREVO_API_URL, json=payload, headers=headers, timeout=10.0)
        response.raise_for_status()


async def send_otp_email(email: str, code: str, purpose: str) -> None:
    await _send_email(
        to_email=email,
        subject="Your Student Progress Tracker verification code",
        text_content=f"Your verification code is: {code}\n\nUse this code to {purpose}. It will expire shortly.",
    )


async def send_password_reset_email(email: str, reset_link: str) -> None:
    await _send_email(
        to_email=email,
        subject="Reset your Student Progress Tracker password",
        text_content=(
            f"We received a request to reset your password.\n\n"
            f"Click the link below to set a new password:\n{reset_link}\n\n"
            f"This link expires in 15 minutes. If you didn't request this, ignore this email."
        ),
    )

async def send_digest_email(email: str, name: str, digest_text: str) -> None:
    await _send_email(
        to_email=email,
        subject="Your weekly study summary",
        text_content=f"Hi {name},\n\n{digest_text}\n\nKeep up the momentum!",
    )