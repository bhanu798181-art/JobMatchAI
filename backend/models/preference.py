from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Preference(Base):
    __tablename__ = "preferences"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "student_profiles.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        unique=True
    )

    preferred_roles: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    preferred_locations: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    work_mode: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    employment_type: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    min_salary: Mapped[int | None] = mapped_column(
        Integer,
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