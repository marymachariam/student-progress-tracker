import time
from app.repositories import analytics as analytics_repo
from app.core.ai_client import generate_recommendation_text

_cache: dict[int, dict] = {}  


def _build_fallback_text(context: dict) -> str:
    topic = context.get("weakest_topic")
    if topic:
        return (
            f"Your weakest topic right now is {topic['topic']} "
            f"(average {topic['average_score_percent']}%). Consider reviewing it next."
        )
    alerts = context.get("alerts", [])
    if alerts:
        first = alerts[0]
        if first["type"] == "subject_inactive":
            return f"You haven't studied {first['subject']} in {first['days_since_last_session']} days — worth revisiting."
        if first["type"] == "goal_behind_schedule":
            return f"Your goal \"{first['goal']}\" is falling behind schedule — try to catch up soon."
    return "Keep logging study sessions and quiz scores so we can give you a personalized recommendation."


async def get_recommendation(db, student_id: int) -> dict:
    from app.services.analytics import get_alerts, get_weakest_topic

    weakest_topic = get_weakest_topic(db, student_id)
    alerts = get_alerts(db, student_id)
    context = {"weakest_topic": weakest_topic, "alerts": alerts}

    ai_text = await generate_recommendation_text(context)

    if ai_text:
        _cache[student_id] = {"text": ai_text, "generated_at": time.time()}
        return {"recommendation": ai_text, "source": "ai", "based_on": context}

    cached = _cache.get(student_id)
    if cached:
        return {
            "recommendation": cached["text"],
            "source": "cached",
            "based_on": context,
            "cached_at": cached["generated_at"],
        }

    return {"recommendation": _build_fallback_text(context), "source": "fallback", "based_on": context}