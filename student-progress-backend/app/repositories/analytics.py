import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.study_session import StudySession
from app.models.quiz_score import QuizScore
from app.models.goal import Goal
from app.models.subject import Subject
from app.models.topic import Topic


def get_total_hours(db: Session, student_id: int) -> float:
    total = db.query(func.sum(StudySession.hours)).filter(
        StudySession.student_id == student_id
    ).scalar()
    return round(total or 0, 2)


def get_average_quiz_score(db: Session, student_id: int) -> float:
    avg = db.query(func.avg(QuizScore.score * 1.0 / QuizScore.total_marks)).filter(
        QuizScore.student_id == student_id
    ).scalar()
    return round((avg or 0) * 100, 1)


def count_goals(db: Session, student_id: int, is_completed: bool) -> int:
    return db.query(func.count(Goal.goal_id)).filter(
        Goal.student_id == student_id, Goal.is_completed == is_completed
    ).scalar()


def get_top_subject(db: Session, student_id: int) -> str | None:
    row = db.query(Subject.name, func.sum(StudySession.hours).label("total")).join(
        StudySession, StudySession.subject_id == Subject.subject_id
    ).filter(StudySession.student_id == student_id).group_by(
        Subject.subject_id
    ).order_by(func.sum(StudySession.hours).desc()).first()
    return row[0] if row else None


def get_subject_breakdown(db: Session, student_id: int) -> list[tuple[str, float]]:
    rows = db.query(Subject.name, func.sum(StudySession.hours)).join(
        StudySession, StudySession.subject_id == Subject.subject_id
    ).filter(StudySession.student_id == student_id).group_by(
        Subject.subject_id
    ).order_by(func.sum(StudySession.hours).desc()).all()
    return rows


def get_progress_over_time(db: Session, student_id: int) -> list[tuple[str, float]]:
    week = func.date_trunc("week", StudySession.study_date).label("week")
    rows = db.query(week, func.sum(StudySession.hours)).filter(
        StudySession.student_id == student_id
    ).group_by(week).order_by(week).all()
    return [(w.strftime("%Y-%m-%d"), hours) for w, hours in rows]


def get_quiz_trend(db: Session, student_id: int) -> list[tuple[str, float]]:
    rows = db.query(
        Topic.name, func.avg(QuizScore.score * 1.0 / QuizScore.total_marks)
    ).join(Topic, QuizScore.topic_id == Topic.topic_id).filter(
        QuizScore.student_id == student_id
    ).group_by(Topic.topic_id).order_by(
        func.avg(QuizScore.score * 1.0 / QuizScore.total_marks).desc()
    ).all()
    return rows


def get_weakest_topic(db: Session, student_id: int) -> tuple[str, float] | None:
    row = db.query(
        Topic.name, func.avg(QuizScore.score * 1.0 / QuizScore.total_marks)
    ).join(Topic, QuizScore.topic_id == Topic.topic_id).filter(
        QuizScore.student_id == student_id
    ).group_by(Topic.topic_id).order_by(
        func.avg(QuizScore.score * 1.0 / QuizScore.total_marks).asc()
    ).first()
    return row


def get_active_goals(db: Session, student_id: int) -> list[Goal]:
    return db.query(Goal).filter(
        Goal.student_id == student_id, Goal.is_completed == False
    ).all()


def get_goal_by_id(db: Session, goal_id: int, student_id: int) -> Goal | None:
    return db.query(Goal).filter(
        Goal.goal_id == goal_id, Goal.student_id == student_id
    ).first()


def get_hours_since(db: Session, student_id: int, since: datetime.date, until: datetime.date | None = None) -> float:
    query = db.query(func.sum(StudySession.hours)).filter(
        StudySession.student_id == student_id, StudySession.study_date >= since
    )
    if until:
        query = query.filter(StudySession.study_date <= until)
    total = query.scalar()
    return total or 0


def get_sessions_count(db: Session, student_id: int, since: datetime.date, until: datetime.date | None = None) -> int:
    query = db.query(func.count(StudySession.session_id)).filter(
        StudySession.student_id == student_id, StudySession.study_date >= since
    )
    if until:
        query = query.filter(StudySession.study_date <= until)
    return query.scalar() or 0


def get_topics_count(db: Session, student_id: int, since: datetime.date, until: datetime.date | None = None) -> int:
    query = db.query(func.count(func.distinct(StudySession.topic_id))).filter(
        StudySession.student_id == student_id, StudySession.study_date >= since
    )
    if until:
        query = query.filter(StudySession.study_date <= until)
    return query.scalar() or 0


def get_quizzes_count(db: Session, student_id: int, since: datetime.date, until: datetime.date | None = None) -> int:
    query = db.query(func.count(QuizScore.score_id)).filter(
        QuizScore.student_id == student_id, QuizScore.quiz_date >= since
    )
    if until:
        query = query.filter(QuizScore.quiz_date <= until)
    return query.scalar() or 0


def get_distinct_study_dates(db: Session, student_id: int) -> list[datetime.date]:
    rows = db.query(StudySession.study_date).filter(
        StudySession.student_id == student_id
    ).distinct().order_by(StudySession.study_date.desc()).all()
    return [r[0] for r in rows]


def get_subjects_with_last_session(db: Session, student_id: int) -> list[tuple[int, str, datetime.date | None]]:
    rows = db.query(Subject.subject_id, Subject.name).filter(
        Subject.student_id == student_id
    ).all()
    result = []
    for subject_id, name in rows:
        last_date = db.query(func.max(StudySession.study_date)).filter(
            StudySession.subject_id == subject_id, StudySession.student_id == student_id
        ).scalar()
        result.append((subject_id, name, last_date))
    return result


def get_all_quiz_scores(db: Session, student_id: int) -> list[QuizScore]:
    return db.query(QuizScore).filter(QuizScore.student_id == student_id).all()