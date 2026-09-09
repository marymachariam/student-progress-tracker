from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import student as student_repo
from app.schemas.student import StudentCreate, StudentLogin, StudentUpdate, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.models.student import Student
from fastapi import HTTPException, status
from app.core.cloudinary_client import upload_profile_picture
from app.schemas.student import StudentCreate, StudentLogin, StudentUpdate, ChangePasswordRequest, Token

MAX_UPLOAD_SIZE = 5 * 1024 * 1024  
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


def register_student(db: Session, payload: StudentCreate) -> Student:
    if student_repo.get_student_by_email(db, payload.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")

    hashed = hash_password(payload.password)
    return student_repo.create_student(db, payload.name, payload.email, hashed)


def authenticate_student(db: Session, payload: StudentLogin) -> Token:
    student = student_repo.get_student_by_email(db, payload.email)
    if not student or not verify_password(payload.password, student.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")

    if not student.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "This account has been deactivated")

    token = create_access_token({"sub": str(student.student_id)})
    return Token(access_token=token)


def update_student(db: Session, student: Student, payload: StudentUpdate) -> Student:
    updates = payload.model_dump(exclude_unset=True)

    if "email" in updates and updates["email"] != student.email:
        if student_repo.get_student_by_email(db, updates["email"]):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")

    if "password" in updates:
        updates["hashed_password"] = hash_password(updates.pop("password"))

    return student_repo.update_student(db, student, updates)


def delete_student(db: Session, student: Student) -> None:
    student_repo.delete_student(db, student)
    
def deactivate_student(db: Session, student: Student) -> Student:
    return student_repo.update_student(db, student, {"is_active": False})

async def update_profile_picture(db, student, file):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Only JPEG, PNG, or WebP images are allowed")

    contents = await file.read()
    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Image must be under 5MB")

    url = upload_profile_picture(contents, student.student_id)
    student.profile_picture_url = url
    db.commit()
    db.refresh(student)
    return student

async def change_password(db: Session, student: Student, payload: ChangePasswordRequest) -> None:
    if not verify_password(payload.current_password, student.hashed_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Current password is incorrect")

    student.hashed_password = hash_password(payload.new_password)
    db.commit()