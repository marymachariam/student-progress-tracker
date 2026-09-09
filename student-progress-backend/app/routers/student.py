from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from app.core.deps import get_current_student
from app.schemas.student import StudentCreate, StudentLogin, StudentUpdate, StudentResponse, Token
from app.services import student as student_service
from fastapi import UploadFile, File

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


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(db: Session = Depends(get_db), current_student=Depends(get_current_student)):
    student_service.delete_student(db, current_student)
