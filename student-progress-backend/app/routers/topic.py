from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import Query

from database import get_db
from app.core.deps import get_current_student
from app.schemas.topic import TopicCreate, TopicUpdate, TopicResponse
from app.services import topic as topic_service

router = APIRouter(prefix="/topics", tags=["topics"])


@router.post("", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
def create_topic(
    payload: TopicCreate,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return topic_service.create_topic(db, current_student.student_id, payload)


@router.get("", response_model=list[TopicResponse])
def list_topics(
    subject_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return topic_service.get_topics(db, current_student.student_id, subject_id, skip, limit)

@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return topic_service.get_topic(db, topic_id, current_student.student_id)


@router.put("/{topic_id}", response_model=TopicResponse)
def update_topic(
    topic_id: int,
    payload: TopicUpdate,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    return topic_service.update_topic(db, topic_id, current_student.student_id, payload)


@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student),
):
    topic_service.delete_topic(db, topic_id, current_student.student_id)