from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import goal as goal_repo
from app.schemas.goal import GoalCreate, GoalUpdate
from app.models.goal import Goal


def create_goal(db: Session, student_id: int, payload: GoalCreate) -> Goal:
    if payload.start_date > payload.end_date:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "start_date must be before end_date")
    return goal_repo.create_goal(
        db, student_id, payload.title, payload.target_type,
        payload.target_value, payload.start_date, payload.end_date,
    )


def get_goals(db: Session, student_id: int, active_only: bool, skip: int = 0, limit: int = 20) -> list[Goal]:
    if active_only:
        return goal_repo.get_active_goals(db, student_id, skip, limit)
    return goal_repo.get_goals_by_student(db, student_id, skip, limit)

def get_goal(db: Session, goal_id: int, student_id: int) -> Goal:
    goal = goal_repo.get_goal_by_id(db, goal_id, student_id)
    if not goal:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Goal not found")
    return goal


def update_goal(db: Session, goal_id: int, student_id: int, payload: GoalUpdate) -> Goal:
    goal = get_goal(db, goal_id, student_id)
    updates = payload.model_dump(exclude_unset=True)

    start = updates.get("start_date", goal.start_date)
    end = updates.get("end_date", goal.end_date)
    if start > end:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "start_date must be before end_date")

    return goal_repo.update_goal(db, goal, updates)


def delete_goal(db: Session, goal_id: int, student_id: int) -> None:
    goal = get_goal(db, goal_id, student_id)
    goal_repo.delete_goal(db, goal)