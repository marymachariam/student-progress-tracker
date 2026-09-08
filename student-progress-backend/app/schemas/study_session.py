from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict


class StudySessionBase(BaseModel):
    subject_id: int
    topic_id: int
    study_date: date
    hours: float = Field(..., gt=0, le=24)
    notes: str | None = None


class StudySessionCreate(StudySessionBase):
    pass


class StudySessionUpdate(BaseModel):
    subject_id: int | None = None
    topic_id: int | None = None
    study_date: date | None = None
    hours: float | None = Field(None, gt=0, le=24)
    notes: str | None = None


class StudySessionResponse(StudySessionBase):
    session_id: int
    student_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)