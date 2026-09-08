from sqlalchemy.orm import Session
from app.models.topic import Topic


def get_topic_by_id(db: Session, topic_id: int, student_id: int) -> Topic | None:
    return db.query(Topic).filter(
        Topic.topic_id == topic_id, Topic.student_id == student_id
    ).first()


def get_topics_by_student(db: Session, student_id: int, skip: int = 0, limit: int = 20) -> list[Topic]:
    return db.query(Topic).filter(Topic.student_id == student_id).offset(skip).limit(limit).all()

def get_topics_by_subject(db: Session, subject_id: int, student_id: int, skip: int = 0, limit: int = 20) -> list[Topic]:
    return db.query(Topic).filter(
        Topic.subject_id == subject_id, Topic.student_id == student_id
    ).offset(skip).limit(limit).all()


def create_topic(db: Session, student_id: int, subject_id: int, name: str) -> Topic:
    topic = Topic(student_id=student_id, subject_id=subject_id, name=name)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


def update_topic(db: Session, topic: Topic, updates: dict) -> Topic:
    for key, value in updates.items():
        setattr(topic, key, value)
    db.commit()
    db.refresh(topic)
    return topic


def delete_topic(db: Session, topic: Topic) -> None:
    db.delete(topic)
    db.commit()