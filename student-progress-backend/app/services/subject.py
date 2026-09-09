from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import subject as subject_repo
from app.schemas.subject import SubjectCreate, SubjectUpdate
from app.models.subject import Subject


def create_subject(db: Session, student_id: int, payload: SubjectCreate) -> Subject:
    return subject_repo.create_subject(db, student_id, payload.name, payload.color)


def get_subjects(db: Session, student_id: int, skip: int = 0, limit: int = 20) -> list[Subject]:
    return subject_repo.get_subjects_by_student(db, student_id, skip, limit)

def get_subject(db: Session, subject_id: int, student_id: int) -> Subject:
    subject = subject_repo.get_subject_by_id(db, subject_id, student_id)
    if not subject:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Subject not found")
    return subject


def update_subject(db: Session, subject_id: int, student_id: int, payload: SubjectUpdate) -> Subject:
    subject = get_subject(db, subject_id, student_id)
    updates = payload.model_dump(exclude_unset=True)
    return subject_repo.update_subject(db, subject, updates)


def delete_subject(db: Session, subject_id: int, student_id: int) -> None:
    subject = get_subject(db, subject_id, student_id)
    subject_repo.delete_subject(db, subject)