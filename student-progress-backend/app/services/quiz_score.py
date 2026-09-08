from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import quiz_score as quiz_repo
from app.repositories import subject as subject_repo
from app.repositories import topic as topic_repo
from app.schemas.quiz_score import QuizScoreCreate, QuizScoreUpdate
from app.models.quiz_score import QuizScore


def _validate_refs(db: Session, student_id: int, subject_id: int, topic_id: int) -> None:
    if not subject_repo.get_subject_by_id(db, subject_id, student_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Subject not found")
    if not topic_repo.get_topic_by_id(db, topic_id, student_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Topic not found")


def create_quiz_score(db: Session, student_id: int, payload: QuizScoreCreate) -> QuizScore:
    _validate_refs(db, student_id, payload.subject_id, payload.topic_id)
    return quiz_repo.create_quiz_score(
        db, student_id, payload.subject_id, payload.topic_id,
        payload.score, payload.total_marks, payload.quiz_date,
    )


def get_quiz_scores(db: Session, student_id: int, skip: int = 0, limit: int = 20) -> list[QuizScore]:
    return quiz_repo.get_quiz_scores_by_student(db, student_id, skip, limit)

def get_quiz_score(db: Session, score_id: int, student_id: int) -> QuizScore:
    quiz_score = quiz_repo.get_quiz_score_by_id(db, score_id, student_id)
    if not quiz_score:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Quiz score not found")
    return quiz_score


def update_quiz_score(db: Session, score_id: int, student_id: int, payload: QuizScoreUpdate) -> QuizScore:
    quiz_score = get_quiz_score(db, score_id, student_id)
    updates = payload.model_dump(exclude_unset=True)

    subject_id = updates.get("subject_id", quiz_score.subject_id)
    topic_id = updates.get("topic_id", quiz_score.topic_id)
    if "subject_id" in updates or "topic_id" in updates:
        _validate_refs(db, student_id, subject_id, topic_id)

    score = updates.get("score", quiz_score.score)
    total_marks = updates.get("total_marks", quiz_score.total_marks)
    if score > total_marks:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "score cannot exceed total_marks")

    return quiz_repo.update_quiz_score(db, quiz_score, updates)


def delete_quiz_score(db: Session, score_id: int, student_id: int) -> None:
    quiz_score = get_quiz_score(db, score_id, student_id)
    quiz_repo.delete_quiz_score(db, quiz_score)