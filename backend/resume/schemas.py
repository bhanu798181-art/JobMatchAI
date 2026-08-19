from pydantic import BaseModel, Field


class ResumeCreate(BaseModel):
    resume_file: str | None = Field(
        default=None,
        max_length=255
    )

    resume_text: str | None = Field(
        default=None,
        max_length=20000
    )


class ResumeUpdate(BaseModel):
    resume_file: str | None = Field(
        default=None,
        max_length=255
    )

    resume_text: str | None = Field(
        default=None,
        max_length=20000
    )


class ResumeResponse(BaseModel):
    id: int
    user_id: int
    resume_file: str | None
    resume_text: str | None

    model_config = {
        "from_attributes": True
    }