from datetime import date
from sqlalchemy.orm import Session
from app.models.study_session import StudySession


def get_session_by_id(db: Session, session_id: int, student_id: int) -> StudySession | None:
    return db.query(StudySession).filter(
        StudySession.session_id == session_id, StudySession.student_id == student_id
    ).first()


def get_sessions_by_student(db: Session, student_id: int, skip: int = 0, limit: int = 20) -> list[StudySession]:
    return db.query(StudySession).filter(StudySession.student_id == student_id).offset(skip).limit(limit).all()

def get_sessions_since(db: Session, student_id: int, since: date, skip: int = 0, limit: int = 20) -> list[StudySession]:
    return db.query(StudySession).filter(
        StudySession.student_id == student_id, StudySession.study_date >= since
    ).offset(skip).limit(limit).all()


def create_session(
    db: Session,
    student_id: int,
    subject_id: int,
    topic_id: int,
    study_date: date,
    hours: float,
    notes: str | None,
) -> StudySession:
    session = StudySession(
        student_id=student_id,
        subject_id=subject_id,
        topic_id=topic_id,
        study_date=study_date,
        hours=hours,
        notes=notes,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def update_session(db: Session, session: StudySession, updates: dict) -> StudySession:
    for key, value in updates.items():
        setattr(session, key, value)
    db.commit()
    db.refresh(session)
    return session


def delete_session(db: Session, session: StudySession) -> None:
    db.delete(session)
    db.commit()