from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict


class GoalBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    target_type: str = Field(..., max_length=50)  # e.g. "hours"
    target_value: float = Field(..., gt=0)
    start_date: date
    end_date: date


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    target_type: str | None = Field(None, max_length=50)
    target_value: float | None = Field(None, gt=0)
    start_date: date | None = None
    end_date: date | None = None
    is_completed: bool | None = None


class GoalResponse(GoalBase):
    goal_id: int
    student_id: int
    is_completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)