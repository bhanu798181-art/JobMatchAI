from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from models.job_preference import JobPreference
from models.user import User
from preferences.schemas import (
    JobPreferenceCreate,
    JobPreferenceUpdate
)


def create_job_preference(
    db: DBSession,
    user: User,
    data: JobPreferenceCreate
) -> JobPreference:

    # 1. Check whether this user already has job preferences
    existing_preference = db.scalar(
        select(JobPreference).where(
            JobPreference.user_id == user.id
        )
    )

    if existing_preference:
        raise ValueError("Job preference already exists")

    # 2. Create the job preference
    preference = JobPreference(
        user_id=user.id,
        preferred_job_title=data.preferred_job_title,
        skills=data.skills,
        preferred_location=data.preferred_location,
        experience_level=data.experience_level,
        expected_salary=data.expected_salary,
        work_type=data.work_type
    )

    # 3. Add it to the database
    db.add(preference)

    # 4. Save the change
    db.commit()

    # 5. Refresh generated values
    db.refresh(preference)

    return preference


def get_job_preference(
    db: DBSession,
    user: User
) -> JobPreference:

    # Find the job preference belonging to the logged-in user
    preference = db.scalar(
        select(JobPreference).where(
            JobPreference.user_id == user.id
        )
    )

    if not preference:
        raise ValueError("Job preference not found")

    return preference


def update_job_preference(
    db: DBSession,
    user: User,
    data: JobPreferenceUpdate
) -> JobPreference:

    # 1. Find the preference belonging to the logged-in user
    preference = db.scalar(
        select(JobPreference).where(
            JobPreference.user_id == user.id
        )
    )

    # 2. Preference doesn't exist
    if not preference:
        raise ValueError("Job preference not found")

    # 3. Get only fields that were actually provided
    update_data = data.model_dump(
        exclude_unset=True
    )

    # 4. Update each provided field
    for field, value in update_data.items():
        setattr(preference, field, value)

    # 5. Save the changes
    db.commit()

    # 6. Refresh the preference
    db.refresh(preference)

    return preference


def delete_job_preference(
    db: DBSession,
    user: User
) -> None:

    # 1. Find the preference belonging to the logged-in user
    preference = db.scalar(
        select(JobPreference).where(
            JobPreference.user_id == user.id
        )
    )

    # 2. Preference doesn't exist
    if not preference:
        raise ValueError("Job preference not found")

    # 3. Delete the preference
    db.delete(preference)

    # 4. Save the change
    db.commit()