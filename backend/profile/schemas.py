from typing import Literal

from pydantic import BaseModel, Field


# ==================================================
# STUDENT PROFILE
# ==================================================

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


# ==================================================
# SKILL SCHEMAS
# ==================================================

ProficiencyLevel = Literal[
    "Beginner",
    "Intermediate",
    "Advanced",
    "Expert"
]


class SkillResponse(BaseModel):
    id: int
    canonical_name: str
    category: str | None

    model_config = {
        "from_attributes": True
    }


class StudentSkillResponse(BaseModel):
    id: int
    skill_id: int
    canonical_name: str
    category: str | None
    proficiency: ProficiencyLevel | None


class StudentSkillAdd(BaseModel):
    skill_id: int = Field(
        gt=0
    )

    proficiency: ProficiencyLevel | None = None


# ==================================================
# EDUCATION
# ==================================================

class EducationResponse(BaseModel):
    id: int
    student_id: int

    qualification: str
    degree_name: str | None
    branch: str | None
    college: str | None
    graduation_year: int | None
    cgpa: float | None
    percentage: float | None

    model_config = {
        "from_attributes": True
    }
    # ==================================================
# UPDATE EDUCATION
# ==================================================

class EducationUpdate(BaseModel):

    qualification: str | None = Field(
        default=None,
        max_length=50
    )

    degree_name: str | None = Field(
        default=None,
        max_length=255
    )

    branch: str | None = Field(
        default=None,
        max_length=100
    )

    college: str | None = Field(
        default=None,
        max_length=255
    )

    graduation_year: int | None = None

    cgpa: float | None = None

    percentage: float | None = None
    