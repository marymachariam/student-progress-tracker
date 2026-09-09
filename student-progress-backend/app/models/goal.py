from datetime import datetime, date

from sqlalchemy import String, Float, Boolean, ForeignKey, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Goal(Base):
    __tablename__ = "goals"

    goal_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    current_value: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)  
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    student: Mapped["Student"] = relationship("Student", back_populates="goals")