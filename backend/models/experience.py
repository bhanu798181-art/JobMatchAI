from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Experience(Base):
    __tablename__ = "experiences"

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
        nullable=False
    )

    experience_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    company_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    role: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    duration_months: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )