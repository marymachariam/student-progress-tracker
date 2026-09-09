from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_hours_studied: float
    average_quiz_score_percent: float
    active_goals: int
    completed_goals: int
    top_subject: str


class SubjectBreakdownItem(BaseModel):
    subject: str
    hours: float


class ProgressOverTimeItem(BaseModel):
    week: str
    hours: float


class QuizTrendItem(BaseModel):
    topic: str
    average_score_percent: float


class WeakestTopic(BaseModel):
    topic: str
    average_score_percent: float


class GoalProgressItem(BaseModel):
    goal_id: int
    title: str
    target_value: float
    actual_progress: float
    percent_complete: float
    end_date: str


class StudyStreak(BaseModel):
    current_streak_days: int


class GoalPrediction(BaseModel):
    goal_id: int
    target_value: float
    actual_so_far: float
    predicted_final_total: float
    on_track: bool


class AlertItem(BaseModel):
    type: str
    subject: str | None = None
    goal: str | None = None
    expected_by_now: float | None = None
    actual: float | None = None
    days_since_last_session: int | None = None