from datetime import date, datetime

from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    company_id: int

    title: str = Field(
        max_length=255
    )

    description: str | None = None

    responsibilities: str | None = None

    required_skills: list[str] | None = None

    preferred_skills: list[str] | None = None

    education_requirement: str | None = Field(
        default=None,
        max_length=255
    )

    education_accepts_diploma: bool | None = None

    branch_requirement: list[str] | None = None

    experience_requirement: str | None = Field(
        default=None,
        max_length=100
    )

    min_graduation_year: int | None = None

    max_graduation_year: int | None = None

    min_cgpa: float | None = Field(
        default=None,
        ge=0,
        le=10
    )

    min_percentage: float | None = Field(
        default=None,
        ge=0,
        le=100
    )

    location: str | None = Field(
        default=None,
        max_length=255
    )

    work_mode: str | None = Field(
        default=None,
        max_length=20
    )

    salary_min: int | None = None

    salary_max: int | None = None

    employment_type: str | None = Field(
        default=None,
        max_length=20
    )

    posted_date: date

    application_deadline: date | None = None

    application_url: str = Field(
        max_length=500
    )

    source: str | None = Field(
        default=None,
        max_length=100
    )

    source_url: str | None = Field(
        default=None,
        max_length=500
    )

    status: str = Field(
        max_length=20
    )


class JobUpdate(BaseModel):
    company_id: int | None = None

    title: str | None = Field(
        default=None,
        max_length=255
    )

    description: str | None = None

    responsibilities: str | None = None

    required_skills: list[str] | None = None

    preferred_skills: list[str] | None = None

    education_requirement: str | None = Field(
        default=None,
        max_length=255
    )

    education_accepts_diploma: bool | None = None

    branch_requirement: list[str] | None = None

    experience_requirement: str | None = Field(
        default=None,
        max_length=100
    )

    min_graduation_year: int | None = None

    max_graduation_year: int | None = None

    min_cgpa: float | None = Field(
        default=None,
        ge=0,
        le=10
    )

    min_percentage: float | None = Field(
        default=None,
        ge=0,
        le=100
    )

    location: str | None = Field(
        default=None,
        max_length=255
    )

    work_mode: str | None = Field(
        default=None,
        max_length=20
    )

    salary_min: int | None = None

    salary_max: int | None = None

    employment_type: str | None = Field(
        default=None,
        max_length=20
    )

    posted_date: date | None = None

    application_deadline: date | None = None

    application_url: str | None = Field(
        default=None,
        max_length=500
    )

    source: str | None = Field(
        default=None,
        max_length=100
    )

    source_url: str | None = Field(
        default=None,
        max_length=500
    )

    status: str | None = Field(
        default=None,
        max_length=20
    )


class JobResponse(BaseModel):
    id: int
    company_id: int
    title: str
    description: str | None
    responsibilities: str | None
    required_skills: list[str] | None
    preferred_skills: list[str] | None
    education_requirement: str | None
    education_accepts_diploma: bool | None
    branch_requirement: list[str] | None
    experience_requirement: str | None
    min_graduation_year: int | None
    max_graduation_year: int | None
    min_cgpa: float | None
    min_percentage: float | None
    location: str | None
    work_mode: str | None
    salary_min: int | None
    salary_max: int | None
    employment_type: str | None
    posted_date: date
    application_deadline: date | None
    application_url: str
    source: str | None
    source_url: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }