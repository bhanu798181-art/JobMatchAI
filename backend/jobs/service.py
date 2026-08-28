from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from jobs.schemas import JobCreate, JobUpdate
from models.job import Job


# ==================================================
# CREATE JOB
# ==================================================

def create_job(
    db: DBSession,
    data: JobCreate
) -> Job:

    job = Job(
        company_id=data.company_id,
        title=data.title,
        description=data.description,
        responsibilities=data.responsibilities,
        required_skills=data.required_skills,
        preferred_skills=data.preferred_skills,
        education_requirement=data.education_requirement,
        education_accepts_diploma=data.education_accepts_diploma,
        branch_requirement=data.branch_requirement,
        experience_requirement=data.experience_requirement,
        min_graduation_year=data.min_graduation_year,
        max_graduation_year=data.max_graduation_year,
        min_cgpa=data.min_cgpa,
        min_percentage=data.min_percentage,
        location=data.location,
        work_mode=data.work_mode,
        salary_min=data.salary_min,
        salary_max=data.salary_max,
        employment_type=data.employment_type,
        posted_date=data.posted_date,
        application_deadline=data.application_deadline,
        application_url=data.application_url,
        source=data.source,
        source_url=data.source_url,
        status=data.status
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


# ==================================================
# GET ALL JOBS
# ==================================================

def get_jobs(
    db: DBSession
) -> list[Job]:

    jobs = db.scalars(
        select(Job)
        .order_by(
            Job.created_at.desc()
        )
    ).all()

    return list(jobs)


# ==================================================
# GET ONE JOB
# ==================================================

def get_job(
    db: DBSession,
    job_id: int
) -> Job:

    job = db.scalar(
        select(Job).where(
            Job.id == job_id
        )
    )

    if not job:
        raise ValueError(
            "Job not found"
        )

    return job


# ==================================================
# UPDATE COMPANY JOB
# ==================================================

def update_job(
    db: DBSession,
    job_id: int,
    company_id: int,
    data: JobUpdate
) -> Job:

    # Find the job AND make sure it belongs
    # to the logged-in company.
    job = db.scalar(
        select(Job).where(
            Job.id == job_id,
            Job.company_id == company_id
        )
    )

    if not job:
        raise ValueError(
            "Job not found or does not belong to this company"
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    # A company must not be able to move
    # its job to another company.
    update_data.pop(
        "company_id",
        None
    )

    for field, value in update_data.items():
        setattr(
            job,
            field,
            value
        )

    db.commit()
    db.refresh(job)

    return job


# ==================================================
# DELETE COMPANY JOB
# ==================================================

def delete_job(
    db: DBSession,
    job_id: int,
    company_id: int
) -> None:

    # Find the job AND make sure it belongs
    # to the logged-in company.
    job = db.scalar(
        select(Job).where(
            Job.id == job_id,
            Job.company_id == company_id
        )
    )

    if not job:
        raise ValueError(
            "Job not found or does not belong to this company"
        )

    db.delete(job)
    db.commit()