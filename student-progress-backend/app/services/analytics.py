import datetime
from app.repositories import analytics as repo


def get_dashboard_summary(db, student_id: int) -> dict:
    return {
        "total_hours_studied": repo.get_total_hours(db, student_id),
        "average_quiz_score_percent": repo.get_average_quiz_score(db, student_id),
        "active_goals": repo.count_goals(db, student_id, False),
        "completed_goals": repo.count_goals(db, student_id, True),
        "top_subject": repo.get_top_subject(db, student_id) or "None",
    }


def get_subject_breakdown(db, student_id: int) -> list[dict]:
    return [{"subject": name, "hours": hours} for name, hours in repo.get_subject_breakdown(db, student_id)]


def get_progress_over_time(db, student_id: int) -> list[dict]:
    return [{"week": week, "hours": hours} for week, hours in repo.get_progress_over_time(db, student_id)]


def get_quiz_trend(db, student_id: int) -> list[dict]:
    return [
        {"topic": topic, "average_score_percent": round(score * 100, 1)}
        for topic, score in repo.get_quiz_trend(db, student_id)
    ]


def get_weakest_topic(db, student_id: int) -> dict | None:
    row = repo.get_weakest_topic(db, student_id)
    if not row:
        return None
    topic, score = row
    return {"topic": topic, "average_score_percent": round(score * 100, 1)}


def get_goal_progress(db, student_id: int) -> list[dict]:
    goals = repo.get_active_goals(db, student_id)
    result = []
    for goal in goals:
        if goal.target_type == "hours":
            actual = repo.get_hours_since(db, student_id, goal.start_date)
        else:
            actual = 0
        percent = (actual / goal.target_value * 100) if goal.target_value else 0
        result.append({
            "goal_id": goal.goal_id,
            "title": goal.title,
            "target_value": goal.target_value,
            "actual_progress": actual,
            "percent_complete": round(percent, 1),
            "end_date": goal.end_date.isoformat(),
        })
    return result


def get_study_streak(db, student_id: int) -> int:
    dates = set(repo.get_distinct_study_dates(db, student_id))
    streak = 0
    current_day = datetime.date.today()
    while current_day in dates:
        streak += 1
        current_day -= datetime.timedelta(days=1)
    return streak


def get_goal_prediction(db, student_id: int, goal_id: int) -> dict | None:
    goal = repo.get_goal_by_id(db, goal_id, student_id)
    if not goal:
        return None

    actual_so_far = repo.get_hours_since(db, student_id, goal.start_date)

    today = datetime.date.today()
    days_elapsed = max((today - goal.start_date).days, 1)
    days_total = max((goal.end_date - goal.start_date).days, 1)

    daily_avg = actual_so_far / days_elapsed
    predicted_total = daily_avg * days_total

    return {
        "goal_id": goal.goal_id,
        "target_value": goal.target_value,
        "actual_so_far": actual_so_far,
        "predicted_final_total": round(predicted_total, 2),
        "on_track": predicted_total >= goal.target_value,
    }


def get_alerts(db, student_id: int) -> list[dict]:
    alerts = []
    today = datetime.date.today()

    for goal in repo.get_active_goals(db, student_id):
        if goal.target_type != "hours":
            continue
        days_elapsed = max((today - goal.start_date).days, 1)
        days_total = max((goal.end_date - goal.start_date).days, 1)
        expected_progress = goal.target_value * (days_elapsed / days_total)
        actual = repo.get_hours_since(db, student_id, goal.start_date)

        if actual < expected_progress:
            alerts.append({
                "type": "goal_behind_schedule",
                "goal": goal.title,
                "expected_by_now": round(expected_progress, 1),
                "actual": actual,
            })

    for subject_id, name, last_date in repo.get_subjects_with_last_session(db, student_id):
        if last_date is None:
            alerts.append({"type": "no_sessions_logged", "subject": name})
            continue
        days_since = (today - last_date).days
        if days_since >= 3:
            alerts.append({
                "type": "subject_inactive",
                "subject": name,
                "days_since_last_session": days_since,
            })

    return alerts