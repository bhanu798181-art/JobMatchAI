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

    # Check whether this student already applied
    # to this exact job.
    existing_application = db.scalar(
        select(JobApplication).where(
            JobApplication.user_id == user.id,
            JobApplication.job_id == data.job_id,
            JobApplication.job_type == data.job_type
        )
    )

    if existing_application:
        raise ValueError(
            "You have already applied for this job"
        )

    # Create the application
    application = JobApplication(
        user_id=user.id,
        job_id=data.job_id,
        job_type=data.job_type,
        job_title=data.job_title,
        company_name=data.company_name,
        job_location=data.job_location,
        application_status=data.application_status,
        applied_at=data.applied_at,
        notes=data.notes
    )

    # Add it to the database
    db.add(application)

    # Save
    db.commit()

    # Refresh generated values
    db.refresh(application)

    return application


def get_job_applications(
    db: DBSession,
    user: User
) -> list[JobApplication]:

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

    application = db.scalar(
        select(JobApplication).where(
            JobApplication.id == application_id,
            JobApplication.user_id == user.id
        )
    )

    if not application:
        raise ValueError(
            "Job application not found"
        )

    return application


def update_job_application(
    db: DBSession,
    user: User,
    application_id: int,
    data: JobApplicationUpdate
) -> JobApplication:

    application = db.scalar(
        select(JobApplication).where(
            JobApplication.id == application_id,
            JobApplication.user_id == user.id
        )
    )

    if not application:
        raise ValueError(
            "Job application not found"
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            application,
            field,
            value
        )

    db.commit()
    db.refresh(application)

    return application


def delete_job_application(
    db: DBSession,
    user: User,
    application_id: int
) -> None:

    application = db.scalar(
        select(JobApplication).where(
            JobApplication.id == application_id,
            JobApplication.user_id == user.id
        )
    )

    if not application:
        raise ValueError(
            "Job application not found"
        )

    db.delete(application)

    db.commit()