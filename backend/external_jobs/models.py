from datetime import date, datetime

from sqlalchemy import (
    ARRAY,
    Date,
    DateTime,
    Integer,
    String,
    Text,
    func
)
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class ExternalJob(Base):
    __tablename__ = "external_jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    required_skills: Mapped[list[str] | None] = mapped_column(
        ARRAY(String),
        nullable=True
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    work_mode: Mapped[str | None] = mapped_column(
        String(50),
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
        String(50),
        nullable=True
    )

    posted_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    application_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    source_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )

    external_job_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active"
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