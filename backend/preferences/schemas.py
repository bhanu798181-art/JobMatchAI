from pydantic import BaseModel, Field


class JobPreferenceCreate(BaseModel):
    preferred_job_title: str | None = Field(
        default=None,
        max_length=150
    )

    skills: str | None = Field(
        default=None,
        max_length=2000
    )

    preferred_location: str | None = Field(
        default=None,
        max_length=100
    )

    experience_level: str | None = Field(
        default=None,
        max_length=50
    )

    expected_salary: int | None = Field(
        default=None,
        ge=0
    )

    work_type: str | None = Field(
        default=None,
        max_length=30
    )


class JobPreferenceUpdate(BaseModel):
    preferred_job_title: str | None = Field(
        default=None,
        max_length=150
    )

    skills: str | None = Field(
        default=None,
        max_length=2000
    )

    preferred_location: str | None = Field(
        default=None,
        max_length=100
    )

    experience_level: str | None = Field(
        default=None,
        max_length=50
    )

    expected_salary: int | None = Field(
        default=None,
        ge=0
    )

    work_type: str | None = Field(
        default=None,
        max_length=30
    )


class JobPreferenceResponse(BaseModel):
    id: int
    user_id: int
    preferred_job_title: str | None
    skills: str | None
    preferred_location: str | None
    experience_level: str | None
    expected_salary: int | None
    work_type: str | None

    model_config = {
        "from_attributes": True
    }