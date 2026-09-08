from sqlalchemy.orm import Session
from app.models.goal import Goal


def get_goal_by_id(db: Session, goal_id: int, student_id: int) -> Goal | None:
    return db.query(Goal).filter(
        Goal.goal_id == goal_id, Goal.student_id == student_id
    ).first()


def get_goals_by_student(db: Session, student_id: int, skip: int = 0, limit: int = 20) -> list[Goal]:
    return db.query(Goal).filter(Goal.student_id == student_id).offset(skip).limit(limit).all()


def get_active_goals(db: Session, student_id: int, skip: int = 0, limit: int = 20) -> list[Goal]:
    return db.query(Goal).filter(
        Goal.student_id == student_id, Goal.is_completed == False
    ).offset(skip).limit(limit).all()

def create_goal(
    db: Session,
    student_id: int,
    title: str,
    target_type: str,
    target_value: float,
    start_date,
    end_date,
) -> Goal:
    goal = Goal(
        student_id=student_id,
        title=title,
        target_type=target_type,
        target_value=target_value,
        start_date=start_date,
        end_date=end_date,
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


def update_goal(db: Session, goal: Goal, updates: dict) -> Goal:
    for key, value in updates.items():
        setattr(goal, key, value)
    db.commit()
    db.refresh(goal)
    return goal


def delete_goal(db: Session, goal: Goal) -> None:
    db.delete(goal)
    db.commit()