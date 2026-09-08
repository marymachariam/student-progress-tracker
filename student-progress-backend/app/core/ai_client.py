import logging
import httpx

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


async def generate_recommendation_text(context: dict) -> str | None:
    """
    Turns structured analytics data into a short, encouraging recommendation.
    Returns None on any failure so the caller can fall back to a template —
    this should never be the reason a request fails.
    """
    prompt = (
        "You are a supportive study coach. Based on this student's data, "
        "write a short (2-3 sentence), specific, encouraging recommendation "
        "on what to focus on next. Do not use generic filler — reference the "
        "actual topic and numbers given.\n\n"
        f"Data: {context}"
    )

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6,
        "max_tokens": 150,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(GROQ_API_URL, json=payload, headers=headers, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        logger.warning("Groq recommendation call failed, falling back to template: %s", exc)
        return None