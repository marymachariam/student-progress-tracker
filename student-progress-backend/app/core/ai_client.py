import logging
import httpx

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

async def generate_recommendation_text(context: dict) -> str | None:
    prompt = (
        "You are a supportive, knowledgeable study coach helping a student improve. "
        "Based on the data below, write a short, encouraging, and genuinely useful study plan "
        "(4-6 sentences, under 120 words total). Be specific, not generic filler. Include:\n"
        "1. What exactly to focus on and why (reference the actual topic and score).\n"
        "2. A concrete way to study it — e.g. a type of resource (video tutorials, practice "
        "problems, textbook review, active recall flashcards) suited to that kind of topic.\n"
        "3. One realistic next step they could do today (e.g. 'spend 20 minutes reviewing X, "
        "then attempt 5 practice questions').\n\n"
        "Do not recommend a specific named website, paid service, or external link — "
        "describe the type of resource instead, since you cannot verify live URLs.\n\n"
        "Write in plain prose only — do not use markdown formatting such as asterisks, "
        "bold text, bullet points, or headers.\n\n"
        f"Student data: {context}"
    )

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6,
        "max_tokens": 500,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(GROQ_API_URL, json=payload, headers=headers, timeout=15.0)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        logger.warning("Groq recommendation call failed, falling back to template: %s", exc)
        return None