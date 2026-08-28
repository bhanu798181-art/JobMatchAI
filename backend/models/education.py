from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Education(Base):
    __tablename__ = "educations"

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

    qualification: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    degree_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    branch: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    college: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    graduation_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    cgpa: Mapped[float | None] = mapped_column(
        Numeric(4, 2),
        nullable=True
    )

    percentage: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )