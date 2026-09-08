from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import Query

from database import get_db
from app.core.deps import get_current_student
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse
from app.services import goal as goal_service

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(
    payload: GoalCreate,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return goal_service.create_goal(db, current_student.student_id, payload)


@router.get("", response_model=list[GoalResponse])
def list_goals(
    active_only: bool = False,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return goal_service.get_goals(db, current_student.student_id, active_only, skip, limit)

@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return goal_service.get_goal(db, goal_id, current_student.student_id)


@router.put("/{goal_id}", response_model=GoalResponse)
def update_goal(
    goal_id: int,
    payload: GoalUpdate,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return goal_service.update_goal(db, goal_id, current_student.student_id, payload)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    goal_service.delete_goal(db, goal_id, current_student.student_id)