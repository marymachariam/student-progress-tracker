from sqlalchemy.orm import Session
from app.models.quiz_score import QuizScore


def get_quiz_score_by_id(db: Session, score_id: int, student_id: int) -> QuizScore | None:
    return db.query(QuizScore).filter(
        QuizScore.score_id == score_id, QuizScore.student_id == student_id
    ).first()

def get_quiz_scores_by_student(db: Session, student_id: int, skip: int = 0, limit: int = 20) -> list[QuizScore]:
    return db.query(QuizScore).filter(QuizScore.student_id == student_id).offset(skip).limit(limit).all()

def create_quiz_score(
    db: Session,
    student_id: int,
    subject_id: int,
    topic_id: int,
    score: int,
    total_marks: int,
    quiz_date,
) -> QuizScore:
    quiz_score = QuizScore(
        student_id=student_id,
        subject_id=subject_id,
        topic_id=topic_id,
        score=score,
        total_marks=total_marks,
        quiz_date=quiz_date,
    )
    db.add(quiz_score)
    db.commit()
    db.refresh(quiz_score)
    return quiz_score


def update_quiz_score(db: Session, quiz_score: QuizScore, updates: dict) -> QuizScore:
    for key, value in updates.items():
        setattr(quiz_score, key, value)
    db.commit()
    db.refresh(quiz_score)
    return quiz_score


def delete_quiz_score(db: Session, quiz_score: QuizScore) -> None:
    db.delete(quiz_score)
    db.commit()