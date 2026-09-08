from sqlalchemy.orm import Session
from app.models.subject import Subject


def get_subject_by_id(db: Session, subject_id: int, student_id: int) -> Subject | None:
    return db.query(Subject).filter(
        Subject.subject_id == subject_id, Subject.student_id == student_id
    ).first()


def get_subjects_by_student(db: Session, student_id: int, skip: int = 0, limit: int = 20) -> list[Subject]:
    return db.query(Subject).filter(Subject.student_id == student_id).offset(skip).limit(limit).all()

def create_subject(db: Session, student_id: int, name: str, color: str | None) -> Subject:
    subject = Subject(student_id=student_id, name=name, color=color)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


def update_subject(db: Session, subject: Subject, updates: dict) -> Subject:
    for key, value in updates.items():
        setattr(subject, key, value)
    db.commit()
    db.refresh(subject)
    return subject


def delete_subject(db: Session, subject: Subject) -> None:
    db.delete(subject)
    db.commit()