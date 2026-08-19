from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from applications.schemas import (
    JobApplicationCreate,
    JobApplicationUpdate
)
from models.job_application import JobApplication
from models.user import User


def create_job_application(
    db: DBSession,
    user: User,
    data: JobApplicationCreate
) -> JobApplication:

    # 1. Create the job application
    application = JobApplication(
        user_id=user.id,
        job_title=data.job_title,
        company_name=data.company_name,
        job_location=data.job_location,
        application_status=data.application_status,
        applied_at=data.applied_at,
        notes=data.notes
    )

    # 2. Add it to the database
    db.add(application)

    # 3. Save the change
    db.commit()

    # 4. Refresh generated values
    db.refresh(application)

    return application


def get_job_applications(
    db: DBSession,
    user: User
) -> list[JobApplication]:

    # Find all applications belonging to the logged-in user
    applications = db.scalars(
        select(JobApplication)
        .where(
            JobApplication.user_id == user.id
        )
        .order_by(
            JobApplication.created_at.desc()
        )
    ).all()

    return list(applications)


def get_job_application(
    db: DBSession,
    user: User,
    application_id: int
) -> JobApplication:

    # Find one application belonging to the logged-in user
    application = db.scalar(
        select(JobApplication).where(
            JobApplication.id == application_id,
            JobApplication.user_id == user.id
        )
    )

    if not application:
        raise ValueError("Job application not found")

    return application


def update_job_application(
    db: DBSession,
    user: User,
    application_id: int,
    data: JobApplicationUpdate
) -> JobApplication:

    # 1. Find the application
    application = db.scalar(
        select(JobApplication).where(
            JobApplication.id == application_id,
            JobApplication.user_id == user.id
        )
    )

    # 2. Application doesn't exist
    if not application:
        raise ValueError("Job application not found")

    # 3. Get only fields that were actually provided
    update_data = data.model_dump(
        exclude_unset=True
    )

    # 4. Update each provided field
    for field, value in update_data.items():
        setattr(application, field, value)

    # 5. Save the changes
    db.commit()

    # 6. Refresh the application
    db.refresh(application)

    return application


def delete_job_application(
    db: DBSession,
    user: User,
    application_id: int
) -> None:

    # 1. Find the application
    application = db.scalar(
        select(JobApplication).where(
            JobApplication.id == application_id,
            JobApplication.user_id == user.id
        )
    )

    # 2. Application doesn't exist
    if not application:
        raise ValueError("Job application not found")

    # 3. Delete the application
    db.delete(application)

    # 4. Save the change
    db.commit()