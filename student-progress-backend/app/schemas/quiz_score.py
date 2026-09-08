from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict


class QuizScoreBase(BaseModel):
    subject_id: int
    topic_id: int
    score: int = Field(..., ge=0)
    total_marks: int = Field(..., gt=0)
    quiz_date: date


class QuizScoreCreate(QuizScoreBase):
    pass


class QuizScoreUpdate(BaseModel):
    subject_id: int | None = None
    topic_id: int | None = None
    score: int | None = Field(None, ge=0)
    total_marks: int | None = Field(None, gt=0)
    quiz_date: date | None = None


class QuizScoreResponse(QuizScoreBase):
    score_id: int
    student_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)