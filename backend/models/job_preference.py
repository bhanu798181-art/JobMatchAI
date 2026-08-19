from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class JobPreference(Base):
    __tablename__ = "job_preferences"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    preferred_job_title: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    skills: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    preferred_location: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    experience_level: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    expected_salary: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    work_type: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )