from sqlalchemy.orm import Session
from app.models.student import Student


def get_student_by_id(db: Session, student_id: int) -> Student | None:
    return db.query(Student).filter(Student.student_id == student_id).first()


def get_student_by_email(db: Session, email: str) -> Student | None:
    return db.query(Student).filter(Student.email == email).first()


def create_student(db: Session, name: str, email: str, hashed_password: str) -> Student:
    student = Student(name=name, email=email, hashed_password=hashed_password)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def update_student(db: Session, student: Student, updates: dict) -> Student:
    for key, value in updates.items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student: Student) -> None:
    db.delete(student)
    db.commit()