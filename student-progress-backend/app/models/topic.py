from datetime import datetime
from typing import List

from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Topic(Base):
    __tablename__ = "topics"

    topic_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.subject_id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    student: Mapped["Student"] = relationship("Student", back_populates="topics")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="topics")
    study_sessions: Mapped[List["StudySession"]] = relationship(
        "StudySession", back_populates="topic", cascade="all, delete-orphan"
    )
    quiz_scores: Mapped[List["QuizScore"]] = relationship(
        "QuizScore", back_populates="topic", cascade="all, delete-orphan"
    )