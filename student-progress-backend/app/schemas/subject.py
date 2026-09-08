from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class SubjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    color: str | None = Field(None, max_length=20)


class SubjectCreate(SubjectBase):
    pass  # student_id comes from the logged-in user


class SubjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    color: str | None = Field(None, max_length=20)


class SubjectResponse(SubjectBase):
    subject_id: int
    student_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)