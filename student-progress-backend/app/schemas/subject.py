from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class SubjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    color: str | None = Field(None, max_length=20)


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    color: str | None = Field(None, max_length=20)
    is_favorite: bool | None = None


class SubjectResponse(SubjectBase):
    subject_id: int
    student_id: int
    is_favorite: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)