from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Subject(Base):
    __tablename__ = "subjects"

    subject_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    student: Mapped["Student"] = relationship("Student", back_populates="subjects")
    topics: Mapped[List["Topic"]] = relationship(
        "Topic", back_populates="subject", cascade="all, delete-orphan"
    )
    study_sessions: Mapped[List["StudySession"]] = relationship(
        "StudySession", back_populates="subject", cascade="all, delete-orphan"
    )
    quiz_scores: Mapped[List["QuizScore"]] = relationship(
        "QuizScore", back_populates="subject", cascade="all, delete-orphan"
    )