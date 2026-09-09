from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Student(Base):
    __tablename__ = "students"

    student_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    profile_picture_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)  # never store plain text
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    subjects: Mapped[List["Subject"]] = relationship(
        "Subject", back_populates="student", cascade="all, delete-orphan"
    )
    topics: Mapped[List["Topic"]] = relationship(
        "Topic", back_populates="student", cascade="all, delete-orphan"
    )
    study_sessions: Mapped[List["StudySession"]] = relationship(
        "StudySession", back_populates="student", cascade="all, delete-orphan"
    )
    quiz_scores: Mapped[List["QuizScore"]] = relationship(
        "QuizScore", back_populates="student", cascade="all, delete-orphan"
    )
    goals: Mapped[List["Goal"]] = relationship(
        "Goal", back_populates="student", cascade="all, delete-orphan"
    )