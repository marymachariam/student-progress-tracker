from datetime import date
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import Query

from database import get_db
from app.core.deps import get_current_student
from app.schemas.study_session import StudySessionCreate, StudySessionUpdate, StudySessionResponse
from app.services import study_session as session_service

router = APIRouter(prefix="/study-sessions", tags=["study_sessions"])


@router.post("", response_model=StudySessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(
    payload: StudySessionCreate,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return session_service.create_session(db, current_student.student_id, payload)


@router.get("", response_model=list[StudySessionResponse])
def list_sessions(
    since: date | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return session_service.get_sessions(db, current_student.student_id, since, skip, limit)


@router.get("/{session_id}", response_model=StudySessionResponse)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return session_service.get_session(db, session_id, current_student.student_id)


@router.put("/{session_id}", response_model=StudySessionResponse)
def update_session(
    session_id: int,
    payload: StudySessionUpdate,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return session_service.update_session(db, session_id, current_student.student_id, payload)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    session_service.delete_session(db, session_id, current_student.student_id)