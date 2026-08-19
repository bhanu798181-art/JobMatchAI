from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from models.student_profile import StudentProfile
from models.user import User
from profile.schemas import (
    StudentProfileCreate,
    StudentProfileUpdate
)


def create_student_profile(
    db: DBSession,
    user: User,
    data: StudentProfileCreate
) -> StudentProfile:

    # 1. Check whether this user already has a profile
    existing_profile = db.scalar(
        select(StudentProfile).where(
            StudentProfile.user_id == user.id
        )
    )

    if existing_profile:
        raise ValueError("Student profile already exists")

    # 2. Create the profile
    profile = StudentProfile(
        user_id=user.id,
        full_name=data.full_name,
        phone=data.phone,
        city=data.city,
        state=data.state,
        country=data.country
    )

    # 3. Add it to the database
    db.add(profile)

    # 4. Save the change
    db.commit()

    # 5. Refresh generated values
    db.refresh(profile)

    return profile


def get_student_profile(
    db: DBSession,
    user: User
) -> StudentProfile:

    # Find the profile belonging to the logged-in user
    profile = db.scalar(
        select(StudentProfile).where(
            StudentProfile.user_id == user.id
        )
    )

    if not profile:
        raise ValueError("Student profile not found")

    return profile


def update_student_profile(
    db: DBSession,
    user: User,
    data: StudentProfileUpdate
) -> StudentProfile:

    # 1. Find the profile belonging to the logged-in user
    profile = db.scalar(
        select(StudentProfile).where(
            StudentProfile.user_id == user.id
        )
    )

    # 2. Profile doesn't exist
    if not profile:
        raise ValueError("Student profile not found")

    # 3. Get only the fields that were actually provided
    update_data = data.model_dump(
        exclude_unset=True
    )

    # 4. Update each provided field
    for field, value in update_data.items():
        setattr(profile, field, value)

    # 5. Save the changes
    db.commit()

    # 6. Refresh the profile
    db.refresh(profile)

    return profile


def delete_student_profile(
    db: DBSession,
    user: User
) -> None:

    # 1. Find the profile belonging to the logged-in user
    profile = db.scalar(
        select(StudentProfile).where(
            StudentProfile.user_id == user.id
        )
    )

    # 2. Profile doesn't exist
    if not profile:
        raise ValueError("Student profile not found")

    # 3. Delete the profile
    db.delete(profile)

    # 4. Save the change
    db.commit()