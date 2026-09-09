from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import topic as topic_repo
from app.repositories import subject as subject_repo
from app.schemas.topic import TopicCreate, TopicUpdate
from app.models.topic import Topic


def create_topic(db: Session, student_id: int, payload: TopicCreate) -> Topic:
    if not subject_repo.get_subject_by_id(db, payload.subject_id, student_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Subject not found")
    return topic_repo.create_topic(db, student_id, payload.subject_id, payload.name)


def get_topics(db: Session, student_id: int, subject_id: int | None, skip: int = 0, limit: int = 20) -> list[Topic]:
    if subject_id is not None:
        return topic_repo.get_topics_by_subject(db, subject_id, student_id, skip, limit)
    return topic_repo.get_topics_by_student(db, student_id, skip, limit)

def get_topic(db: Session, topic_id: int, student_id: int) -> Topic:
    topic = topic_repo.get_topic_by_id(db, topic_id, student_id)
    if not topic:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Topic not found")
    return topic


def update_topic(db: Session, topic_id: int, student_id: int, payload: TopicUpdate) -> Topic:
    topic = get_topic(db, topic_id, student_id)
    updates = payload.model_dump(exclude_unset=True)

    if "subject_id" in updates and not subject_repo.get_subject_by_id(db, updates["subject_id"], student_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Subject not found")

    return topic_repo.update_topic(db, topic, updates)


def delete_topic(db: Session, topic_id: int, student_id: int) -> None:
    topic = get_topic(db, topic_id, student_id)
    topic_repo.delete_topic(db, topic)