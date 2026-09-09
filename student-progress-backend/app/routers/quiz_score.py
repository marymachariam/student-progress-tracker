from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import Query

from database import get_db
from app.core.deps import get_current_student
from app.schemas.quiz_score import QuizScoreCreate, QuizScoreUpdate, QuizScoreResponse
from app.services import quiz_score as quiz_score_service

router = APIRouter(prefix="/quiz-scores", tags=["quiz_scores"])


@router.post("", response_model=QuizScoreResponse, status_code=status.HTTP_201_CREATED)
def create_quiz_score(
    payload: QuizScoreCreate,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return quiz_score_service.create_quiz_score(db, current_student.student_id, payload)


@router.get("", response_model=list[QuizScoreResponse])
def list_quiz_scores(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return quiz_score_service.get_quiz_scores(db, current_student.student_id, skip, limit)

@router.get("/{score_id}", response_model=QuizScoreResponse)
def get_quiz_score(
    score_id: int,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return quiz_score_service.get_quiz_score(db, score_id, current_student.student_id)


@router.put("/{score_id}", response_model=QuizScoreResponse)
def update_quiz_score(
    score_id: int,
    payload: QuizScoreUpdate,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return quiz_score_service.update_quiz_score(db, score_id, current_student.student_id, payload)


@router.delete("/{score_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz_score(
    score_id: int,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    quiz_score_service.delete_quiz_score(db, score_id, current_student.student_id)