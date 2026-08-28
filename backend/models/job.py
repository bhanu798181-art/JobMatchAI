from datetime import date, datetime

from sqlalchemy import (
    ARRAY,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func
)
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "company_profiles.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    responsibilities: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    required_skills: Mapped[list[str] | None] = mapped_column(
        ARRAY(String),
        nullable=True
    )

    preferred_skills: Mapped[list[str] | None] = mapped_column(
        ARRAY(String),
        nullable=True
    )

    education_requirement: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    education_accepts_diploma: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True
    )

    branch_requirement: Mapped[list[str] | None] = mapped_column(
        ARRAY(String),
        nullable=True
    )

    experience_requirement: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    min_graduation_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    max_graduation_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    min_cgpa: Mapped[float | None] = mapped_column(
        Numeric(4, 2),
        nullable=True
    )

    min_percentage: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    work_mode: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    salary_min: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    salary_max: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    employment_type: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    posted_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    application_deadline: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    application_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    source: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    source_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
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