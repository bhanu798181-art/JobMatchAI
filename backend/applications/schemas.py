from datetime import datetime

from pydantic import BaseModel, Field


class JobApplicationCreate(BaseModel):
    job_title: str = Field(
        max_length=150
    )

    company_name: str = Field(
        max_length=150
    )

    job_location: str | None = Field(
        default=None,
        max_length=100
    )

    application_status: str = Field(
        default="Applied",
        max_length=30
    )

    applied_at: datetime | None = None

    notes: str | None = Field(
        default=None,
        max_length=5000
    )


class JobApplicationUpdate(BaseModel):
    job_title: str | None = Field(
        default=None,
        max_length=150
    )

    company_name: str | None = Field(
        default=None,
        max_length=150
    )

    job_location: str | None = Field(
        default=None,
        max_length=100
    )

    application_status: str | None = Field(
        default=None,
        max_length=30
    )

    applied_at: datetime | None = None

    notes: str | None = Field(
        default=None,
        max_length=5000
    )


class JobApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_title: str
    company_name: str
    job_location: str | None
    application_status: str
    applied_at: datetime | None
    notes: str | None

    model_config = {
        "from_attributes": True
    }