from sqlalchemy.orm import Session

from app.models.student import Student
from app.services.analytics import (
    get_dashboard_summary, get_quiz_trend, get_goal_progress, get_alerts,
)


def build_digest_text(db: Session, student: Student) -> str:
    summary = get_dashboard_summary(db, student.student_id)
    goals = get_goal_progress(db, student.student_id)
    alerts = get_alerts(db, student.student_id)

    lines = [
        f"This week you studied {summary['total_hours_studied']} hours total, "
        f"averaging {summary['average_quiz_score_percent']}% on quizzes.",
        f"Top subject: {summary['top_subject']}. "
        f"Active goals: {summary['active_goals']}, completed: {summary['completed_goals']}.",
    ]

    if goals:
        top_goal = goals[0]
        lines.append(
            f"Goal progress on \"{top_goal['title']}\": {top_goal['percent_complete']}% complete."
        )

    if alerts:
        first = alerts[0]
        if first["type"] == "goal_behind_schedule":
            lines.append(f"Heads up: \"{first['goal']}\" is falling behind schedule.")
        elif first["type"] == "subject_inactive":
            lines.append(f"You haven't touched {first['subject']} in {first['days_since_last_session']} days.")

    return " ".join(lines)


async def send_weekly_digests(db: Session) -> int:
    """Sends a digest to every verified student. Returns count sent."""
    from app.core.mail import send_digest_email

    students = db.query(Student).filter(Student.is_verified == True).all()
    sent = 0
    for student in students:
        digest_text = build_digest_text(db, student)
        await send_digest_email(student.email, student.name, digest_text)
        sent += 1
    return sent