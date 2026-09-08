from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import study_session as session_repo
from app.repositories import subject as subject_repo
from app.repositories import topic as topic_repo
from app.schemas.study_session import StudySessionCreate, StudySessionUpdate
from app.models.study_session import StudySession


def _validate_refs(db: Session, student_id: int, subject_id: int, topic_id: int) -> None:
    if not subject_repo.get_subject_by_id(db, subject_id, student_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Subject not found")
    if not topic_repo.get_topic_by_id(db, topic_id, student_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Topic not found")


def create_session(db: Session, student_id: int, payload: StudySessionCreate) -> StudySession:
    _validate_refs(db, student_id, payload.subject_id, payload.topic_id)
    return session_repo.create_session(
        db, student_id, payload.subject_id, payload.topic_id,
        payload.study_date, payload.hours, payload.notes,
    )

def get_sessions(db: Session, student_id: int, since: date | None, skip: int = 0, limit: int = 20) -> list[StudySession]:
    if since is not None:
        return session_repo.get_sessions_since(db, student_id, since, skip, limit)
    return session_repo.get_sessions_by_student(db, student_id, skip, limit)

def get_session(db: Session, session_id: int, student_id: int) -> StudySession:
    session = session_repo.get_session_by_id(db, session_id, student_id)
    if not session:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Study session not found")
    return session


def update_session(db: Session, session_id: int, student_id: int, payload: StudySessionUpdate) -> StudySession:
    session = get_session(db, session_id, student_id)
    updates = payload.model_dump(exclude_unset=True)

    subject_id = updates.get("subject_id", session.subject_id)
    topic_id = updates.get("topic_id", session.topic_id)
    if "subject_id" in updates or "topic_id" in updates:
        _validate_refs(db, student_id, subject_id, topic_id)

    return session_repo.update_session(db, session, updates)


def delete_session(db: Session, session_id: int, student_id: int) -> None:
    session = get_session(db, session_id, student_id)
    session_repo.delete_session(db, session)