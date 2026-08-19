from pydantic import BaseModel, Field


class StudentProfileCreate(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=255
    )

    phone: str | None = Field(
        default=None,
        max_length=20
    )

    city: str | None = Field(
        default=None,
        max_length=100
    )

    state: str | None = Field(
        default=None,
        max_length=100
    )

    country: str | None = Field(
        default=None,
        max_length=100
    )


class StudentProfileUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255
    )

    phone: str | None = Field(
        default=None,
        max_length=20
    )

    city: str | None = Field(
        default=None,
        max_length=100
    )

    state: str | None = Field(
        default=None,
        max_length=100
    )

    country: str | None = Field(
        default=None,
        max_length=100
    )


class StudentProfileResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    phone: str | None
    city: str | None
    state: str | None
    country: str | None

    model_config = {
        "from_attributes": True
    }