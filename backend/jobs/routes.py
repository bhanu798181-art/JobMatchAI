from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.service import get_user_from_session
from database import get_db

from models.company_profile import CompanyProfile
from models.job import Job

from jobs.schemas import (
    JobCreate,
    JobResponse,
    JobUpdate
)

from jobs.service import (
    create_job,
    get_jobs,
    get_job,
    update_job,
    delete_job
)


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# ==================================================
# CREATE JOB
# ==================================================

@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED
)
def create_job_route(
    data: JobCreate,
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):

    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:

        user = get_user_from_session(
            db,
            session_token
        )

        if user.role != "company":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only companies can create jobs"
            )

        company = db.scalar(
            select(CompanyProfile).where(
                CompanyProfile.user_id == user.id
            )
        )

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found"
            )

        if data.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create jobs for your own company"
            )

        job = create_job(
            db,
            data
        )

        return job

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


# ==================================================
# GET MY COMPANY JOBS
# IMPORTANT:
# This route MUST be before /{job_id}
# ==================================================

@router.get(
    "/my",
    response_model=list[JobResponse],
    status_code=status.HTTP_200_OK
)
def get_my_jobs_route(
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):

    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:

        user = get_user_from_session(
            db,
            session_token
        )

        if user.role != "company":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only companies can access company jobs"
            )

        company = db.scalar(
            select(CompanyProfile).where(
                CompanyProfile.user_id == user.id
            )
        )

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found"
            )

        jobs = db.scalars(
            select(Job)
            .where(
                Job.company_id == company.id
            )
            .order_by(
                Job.id.desc()
            )
        ).all()

        return list(jobs)

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )


# ==================================================
# GET ALL JOBS
# ==================================================

@router.get(
    "",
    response_model=list[JobResponse],
    status_code=status.HTTP_200_OK
)
def get_jobs_route(
    db: Session = Depends(get_db)
):

    return get_jobs(
        db
    )


# ==================================================
# GET ONE JOB
# ==================================================

@router.get(
    "/{job_id}",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK
)
def get_job_route(
    job_id: int,
    db: Session = Depends(get_db)
):

    try:

        return get_job(
            db,
            job_id
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


# ==================================================
# UPDATE JOB
# ==================================================

@router.put(
    "/{job_id}",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK
)
def update_job_route(
    job_id: int,
    data: JobUpdate,
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):

    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:

        user = get_user_from_session(
            db,
            session_token
        )

        if user.role != "company":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only companies can update jobs"
            )

        company = db.scalar(
            select(CompanyProfile).where(
                CompanyProfile.user_id == user.id
            )
        )

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found"
            )

        job = get_job(
            db,
            job_id
        )

        if job.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own jobs"
            )

        if data.company_id is not None:

            if data.company_id != company.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only use your own company profile"
                )

        job = update_job(
            db,
            job_id,
            data
        )

        return job

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


# ==================================================
# DELETE JOB
# ==================================================

@router.delete(
    "/{job_id}",
    status_code=status.HTTP_200_OK
)
def delete_job_route(
    job_id: int,
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):

    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:

        user = get_user_from_session(
            db,
            session_token
        )

        if user.role != "company":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only companies can delete jobs"
            )

        company = db.scalar(
            select(CompanyProfile).where(
                CompanyProfile.user_id == user.id
            )
        )

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found"
            )

        job = get_job(
            db,
            job_id
        )

        if job.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own jobs"
            )

        delete_job(
            db,
            job_id
        )

        return {
            "message": "Job deleted successfully"
        }

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )