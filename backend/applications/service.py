from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from applications.schemas import (
    JobApplicationCreate,
    JobApplicationUpdate
)
from models.job_application import JobApplication
from models.user import User
from models.job import Job


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
def update_company_application_status(
    db: DBSession,
    company: User,
    application_id: int,
    status_value: str
) -> JobApplication:

    result = db.execute(
        select(JobApplication, Job)
        .join(
            Job,
            JobApplication.job_id == Job.id
        )
        .where(
            JobApplication.id == application_id,
            JobApplication.job_type == "internal"
        )
    ).first()

    if not result:
        raise ValueError(
            "Application not found"
        )

    application, job = result

    from models.company_profile import CompanyProfile

    company_profile = db.scalar(
        select(CompanyProfile).where(
            CompanyProfile.user_id == company.id
        )
    )

    if not company_profile:
        raise ValueError(
            "Company profile not found"
        )

    if job.company_id != company_profile.id:
        raise ValueError(
            "You can only manage applications for your own jobs"
        )

    allowed_statuses = {
        "Applied",
        "Reviewing",
        "Shortlisted",
        "Interview",
        "Selected",
        "Rejected"
    }

    if status_value not in allowed_statuses:
        raise ValueError(
            "Invalid application status"
        )

    application.application_status = status_value

    db.commit()
    db.refresh(application)

    return application