from datetime import datetime, date

from sqlalchemy import Integer, ForeignKey, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class QuizScore(Base):
    __tablename__ = "quiz_scores"

    score_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.subject_id", ondelete="CASCADE"), nullable=False, index=True
    )
    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.topic_id", ondelete="CASCADE"), nullable=False, index=True
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    total_marks: Mapped[int] = mapped_column(Integer, nullable=False)
    quiz_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    student: Mapped["Student"] = relationship("Student", back_populates="quiz_scores")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="quiz_scores")
    topic: Mapped["Topic"] = relationship("Topic", back_populates="quiz_scores")