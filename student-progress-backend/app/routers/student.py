from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from app.core.deps import get_current_student
from app.schemas.student import StudentCreate, StudentLogin, StudentUpdate, StudentResponse, Token
from app.services import student as student_service
from fastapi import UploadFile, File
from fastapi import BackgroundTasks
from app.schemas.student import ChangePasswordRequest
from app.core.mail import send_password_changed_email
from app.core.mail import send_password_changed_email, send_account_deactivated_email, send_account_deleted_email


router = APIRouter(prefix="/students", tags=["students"])


@router.post("/register", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def register(payload: StudentCreate, db: Session = Depends(get_db)):
    return student_service.register_student(db, payload)


@router.post("/login", response_model=Token)
def login(payload: StudentLogin, db: Session = Depends(get_db)):
    return student_service.authenticate_student(db, payload)


@router.get("/me", response_model=StudentResponse)
def get_me(current_student=Depends(get_current_student)):
    return current_student

@router.post("/me/picture", response_model=StudentResponse)
async def upload_picture(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return await student_service.update_profile_picture(db, current_student, file)

@router.put("/me", response_model=StudentResponse)
def update_me(
    payload: StudentUpdate,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return student_service.update_student(db, current_student, payload)

@router.post("/me/deactivate", response_model=StudentResponse)
def deactivate_me(db: Session = Depends(get_db), current_student=Depends(get_current_student)):
    return student_service.deactivate_student(db, current_student)

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(db: Session = Depends(get_db), current_student=Depends(get_current_student)):
    student_service.delete_student(db, current_student)
    

@router.post("/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    payload: ChangePasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    await student_service.change_password(db, current_student, payload)
    background_tasks.add_task(send_password_changed_email, current_student.email, current_student.name)

@router.post("/me/deactivate", response_model=StudentResponse)
def deactivate_me(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    updated = student_service.deactivate_student(db, current_student)
    background_tasks.add_task(send_account_deactivated_email, updated.email, updated.name)
    return updated


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    email, name = current_student.email, current_student.name
    student_service.delete_student(db, current_student)
    background_tasks.add_task(send_account_deleted_email, email, name)