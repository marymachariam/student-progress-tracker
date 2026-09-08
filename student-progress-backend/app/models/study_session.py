from datetime import datetime, date
from typing import Optional

from sqlalchemy import Float, Text, ForeignKey, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class StudySession(Base):
    __tablename__ = "study_sessions"

    session_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.subject_id", ondelete="CASCADE"), nullable=False, index=True
    )
    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.topic_id", ondelete="CASCADE"), nullable=False, index=True
    )
    study_date: Mapped[date] = mapped_column(Date, nullable=False)
    hours: Mapped[float] = mapped_column(Float, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    student: Mapped["Student"] = relationship("Student", back_populates="study_sessions")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="study_sessions")
    topic: Mapped["Topic"] = relationship("Topic", back_populates="study_sessions")