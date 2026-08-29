from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession
from models.education import Education

from models.student_profile import StudentProfile
from models.user import User
from models.student_skill import StudentSkill
from models.skill_master import SkillMaster

from profile.schemas import (
    StudentProfileCreate,
    StudentProfileUpdate,
    EducationUpdate
)


# ==================================================
# STUDENT PROFILE
# ==================================================

def create_student_profile(
    db: DBSession,
    user: User,
    data: StudentProfileCreate
) -> StudentProfile:

    existing_profile = db.scalar(
        select(StudentProfile).where(
            
            StudentProfile.user_id == user.id
        )
    )

    if existing_profile:
        raise ValueError(
            "Student profile already exists"
        )

    profile = StudentProfile(
        user_id=user.id,
        full_name=data.full_name,
        phone=data.phone,
        city=data.city,
        state=data.state,
        country=data.country
    )

    db.add(profile)

    db.commit()

    db.refresh(profile)

    return profile


def get_student_profile(
    db: DBSession,
    user: User
) -> StudentProfile:

    profile = db.scalar(
        select(StudentProfile).where(
            StudentProfile.user_id == user.id
        )
    )

    if not profile:
        raise ValueError(
            "Student profile not found"
        )

    return profile


def update_student_profile(
    db: DBSession,
    user: User,
    data: StudentProfileUpdate
) -> StudentProfile:

    profile = db.scalar(
        select(StudentProfile).where(
            StudentProfile.user_id == user.id
        )
    )

    if not profile:
        raise ValueError(
            "Student profile not found"
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            profile,
            field,
            value
        )

    db.commit()

    db.refresh(profile)

    return profile


def delete_student_profile(
    db: DBSession,
    user: User
) -> None:

    profile = db.scalar(
        select(StudentProfile).where(
            StudentProfile.user_id == user.id
        )
    )

    if not profile:
        raise ValueError(
            "Student profile not found"
        )

    db.delete(profile)

    db.commit()


# ==================================================
# SKILLS
# ==================================================

def get_all_skills(
    db: DBSession
) -> list[SkillMaster]:

    skills = db.scalars(
        select(SkillMaster).order_by(
            SkillMaster.canonical_name
        )
    ).all()

    return list(skills)


def get_student_skills(
    db: DBSession,
    user: User
) -> list[dict]:

    profile = db.scalar(
        select(StudentProfile).where(
            StudentProfile.user_id == user.id
        )
    )

    if not profile:
        raise ValueError(
            "Student profile not found"
        )

    rows = db.execute(
        select(
            StudentSkill,
            SkillMaster
        )
        .join(
            SkillMaster,
            StudentSkill.skill_id == SkillMaster.id
        )
        .where(
            StudentSkill.student_id == profile.id
        )
        .order_by(
            SkillMaster.canonical_name
        )
    ).all()

    result = []

    for student_skill, skill in rows:

        result.append(
            {
                "id": student_skill.id,
                "skill_id": skill.id,
                "canonical_name": skill.canonical_name,
                "category": skill.category,
                "proficiency": student_skill.proficiency
            }
        )

    return result


def add_student_skill(
    db: DBSession,
    user: User,
    skill_id: int,
    proficiency: str | None
) -> dict:

    profile = db.scalar(
        select(StudentProfile).where(
            StudentProfile.user_id == user.id
        )
    )

    if not profile:
        raise ValueError(
            "Student profile not found"
        )

    skill = db.scalar(
        select(SkillMaster).where(
            SkillMaster.id == skill_id
        )
    )

    if not skill:
        raise ValueError(
            "Skill not found"
        )

    existing = db.scalar(
        select(StudentSkill).where(
            StudentSkill.student_id == profile.id,
            StudentSkill.skill_id == skill_id
        )
    )

    if existing:
        raise ValueError(
            "Skill already added to your profile"
        )

    student_skill = StudentSkill(
        student_id=profile.id,
        skill_id=skill_id,
        proficiency=proficiency
    )

    db.add(student_skill)

    db.commit()

    db.refresh(student_skill)

    return {
        "id": student_skill.id,
        "skill_id": skill.id,
        "canonical_name": skill.canonical_name,
        "category": skill.category,
        "proficiency": student_skill.proficiency
    }


def remove_student_skill(
    db: DBSession,
    user: User,
    skill_id: int
) -> None:

    profile = db.scalar(
        select(StudentProfile).where(
            StudentProfile.user_id == user.id
        )
    )

    if not profile:
        raise ValueError(
            "Student profile not found"
        )

    student_skill = db.scalar(
        select(StudentSkill).where(
            StudentSkill.student_id == profile.id,
            StudentSkill.skill_id == skill_id
        )
    )

    if not student_skill:
        raise ValueError(
            "Student skill not found"
        )

    db.delete(student_skill)

    db.commit()
    # ==================================================
# GET STUDENT EDUCATION
# ==================================================

def get_student_education(
    db: DBSession,
    user: User
) -> list[Education]:

    student = db.scalar(
        select(StudentProfile).where(
            StudentProfile.user_id == user.id
        )
    )

    if not student:
        raise ValueError(
            "Student profile not found"
        )

    education = db.scalars(
        select(Education)
        .where(
            Education.student_id == student.id
        )
        .order_by(
            Education.created_at.desc()
        )
    ).all()

    return list(education)

# ==================================================
# CREATE STUDENT EDUCATION
# ==================================================

def create_student_education(
    db: DBSession,
    user: User,
    data: EducationUpdate
) -> Education:

    student = db.scalar(
        select(StudentProfile).where(
            StudentProfile.user_id == user.id
        )
    )

    if not student:
        raise ValueError(
            "Student profile not found"
        )

    education_data = data.model_dump(
        exclude_unset=True
    )

    education = Education(
        student_id=student.id,
        **education_data
    )

    db.add(education)

    db.commit()
    db.refresh(education)

    return education
# ==================================================
# UPDATE STUDENT EDUCATION
# ==================================================

def update_student_education(
    db: DBSession,
    user: User,
    education_id: int,
    data: EducationUpdate
) -> Education:

    student = db.scalar(
        select(StudentProfile).where(
            StudentProfile.user_id == user.id
        )
    )

    if not student:
        raise ValueError(
            "Student profile not found"
        )

    education = db.scalar(
        select(Education).where(
            Education.id == education_id,
            Education.student_id == student.id
        )
    )

    if not education:
        raise ValueError(
            "Education record not found"
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():

        setattr(
            education,
            field,
            value
        )

    db.commit()
    db.refresh(education)

    return education