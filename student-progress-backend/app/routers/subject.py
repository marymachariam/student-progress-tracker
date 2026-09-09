from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import Query

from database import get_db
from app.core.deps import get_current_student
from app.schemas.subject import SubjectCreate, SubjectUpdate, SubjectResponse
from app.services import subject as subject_service

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.post("", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(
    payload: SubjectCreate,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return subject_service.create_subject(db, current_student.student_id, payload)


@router.get("", response_model=list[SubjectResponse])
def list_subjects(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return subject_service.get_subjects(db, current_student.student_id, skip, limit)

@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return subject_service.get_subject(db, subject_id, current_student.student_id)


@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: int,
    payload: SubjectUpdate,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return subject_service.update_subject(db, subject_id, current_student.student_id, payload)


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    subject_service.delete_subject(db, subject_id, current_student.student_id)