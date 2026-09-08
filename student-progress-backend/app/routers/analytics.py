from fastapi import APIRouter, HTTPException, status

from app.core.deps import DBSession, CurrentStudent
from app.schemas.analytics import (
    DashboardSummary, SubjectBreakdownItem, ProgressOverTimeItem,
    QuizTrendItem, WeakestTopic, GoalProgressItem, StudyStreak,
    GoalPrediction, AlertItem,
)
from app.services import analytics as analytics_service

router = APIRouter(prefix="/dashboard", tags=["analytics"])


@router.get("", response_model=DashboardSummary)
def dashboard(db: DBSession, current_student: CurrentStudent):
    return analytics_service.get_dashboard_summary(db, current_student.student_id)


@router.get("/subject-breakdown", response_model=list[SubjectBreakdownItem])
def subject_breakdown(db: DBSession, current_student: CurrentStudent):
    return analytics_service.get_subject_breakdown(db, current_student.student_id)


@router.get("/progress-over-time", response_model=list[ProgressOverTimeItem])
def progress_over_time(db: DBSession, current_student: CurrentStudent):
    return analytics_service.get_progress_over_time(db, current_student.student_id)


@router.get("/quiz-trend", response_model=list[QuizTrendItem])
def quiz_trend(db: DBSession, current_student: CurrentStudent):
    return analytics_service.get_quiz_trend(db, current_student.student_id)


@router.get("/weakest-topic", response_model=WeakestTopic | None)
def weakest_topic(db: DBSession, current_student: CurrentStudent):
    return analytics_service.get_weakest_topic(db, current_student.student_id)


@router.get("/goal-progress", response_model=list[GoalProgressItem])
def goal_progress(db: DBSession, current_student: CurrentStudent):
    return analytics_service.get_goal_progress(db, current_student.student_id)


@router.get("/study-streak", response_model=StudyStreak)
def study_streak(db: DBSession, current_student: CurrentStudent):
    return {"current_streak_days": analytics_service.get_study_streak(db, current_student.student_id)}


@router.get("/prediction/{goal_id}", response_model=GoalPrediction)
def goal_prediction(goal_id: int, db: DBSession, current_student: CurrentStudent):
    result = analytics_service.get_goal_prediction(db, current_student.student_id, goal_id)
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Goal not found")
    return result


@router.get("/alerts", response_model=list[AlertItem])
def alerts(db: DBSession, current_student: CurrentStudent):
    return analytics_service.get_alerts(db, current_student.student_id)