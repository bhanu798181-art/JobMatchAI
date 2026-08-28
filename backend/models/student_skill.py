from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class StudentSkill(Base):
    __tablename__ = "student_skills"

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

    skill_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "skills_master.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    proficiency: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )