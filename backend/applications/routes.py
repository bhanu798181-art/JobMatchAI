from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.service import get_user_from_session

from applications.schemas import (
    JobApplicationCreate,
    JobApplicationResponse,
    JobApplicationUpdate,
    CompanyApplicationResponse
)

from applications.service import (
    create_job_application,
    get_job_applications,
    get_job_application,
    update_job_application,
    delete_job_application,
    update_company_application_status
)

from database import get_db

from models.company_profile import CompanyProfile
from models.job_application import JobApplication
from models.job import Job
from models.user import User
from models.student_profile import StudentProfile


router = APIRouter(
    prefix="/applications",
    tags=["Job Applications"]
)


# ==================================================
# COMPANY APPLICATION STATUS SCHEMA
# ==================================================

class CompanyApplicationStatusUpdate(BaseModel):
    application_status: str


# ==================================================
# CREATE APPLICATION
# ==================================================

@router.post(
    "",
    response_model=JobApplicationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_application(
    data: JobApplicationCreate,
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

        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can create job applications"
            )

        application = create_job_application(
            db,
            user,
            data
        )

        return application

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


# ==================================================
# GET STUDENT APPLICATIONS
# ==================================================

@router.get(
    "",
    response_model=list[JobApplicationResponse],
    status_code=status.HTTP_200_OK
)
def get_applications(
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

        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can access job applications"
            )

        applications = get_job_applications(
            db,
            user
        )

        return applications

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


# ==================================================
# GET COMPANY APPLICATIONS
# ==================================================

@router.get(
    "/company",
    response_model=list[CompanyApplicationResponse],
    status_code=status.HTTP_200_OK
)
def get_company_applications(
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
                detail="Only companies can access received applications"
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

        rows = db.execute(
            select(
                JobApplication,
                User.email,
                StudentProfile.full_name
            )
            .join(
                Job,
                JobApplication.job_id == Job.id
            )
            .join(
                User,
                JobApplication.user_id == User.id
            )
            .outerjoin(
                StudentProfile,
                StudentProfile.user_id == User.id
            )
            .where(
                Job.company_id == company.id,
                JobApplication.job_type == "internal"
            )
            .order_by(
                JobApplication.id.desc()
            )
        ).all()

        return [
            {
                "id": application.id,
                "user_id": application.user_id,
                "student_name": full_name,
                "student_email": email,
                "job_id": application.job_id,
                "job_type": application.job_type,
                "job_title": application.job_title,
                "company_name": application.company_name,
                "job_location": application.job_location,
                "application_status": application.application_status,
                "applied_at": application.applied_at,
                "notes": application.notes,
            }
            for application, email, full_name in rows
        ]

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )


# ==================================================
# COMPANY UPDATE APPLICATION STATUS
# IMPORTANT:
# This route MUST be before /{application_id}
# ==================================================

@router.put(
    "/company/{application_id}/status",
    response_model=JobApplicationResponse,
    status_code=status.HTTP_200_OK
)
def update_company_application_status_route(
    application_id: int,
    data: CompanyApplicationStatusUpdate,
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
                detail="Only companies can update application status"
            )

        application = update_company_application_status(
            db,
            user,
            application_id,
            data.application_status
        )

        return application

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


# ==================================================
# GET ONE APPLICATION
# ==================================================

@router.get(
    "/{application_id}",
    response_model=JobApplicationResponse,
    status_code=status.HTTP_200_OK
)
def get_application(
    application_id: int,
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

        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can access job applications"
            )

        application = get_job_application(
            db,
            user,
            application_id
        )

        return application

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


# ==================================================
# UPDATE STUDENT APPLICATION
# ==================================================

@router.put(
    "/{application_id}",
    response_model=JobApplicationResponse,
    status_code=status.HTTP_200_OK
)
def update_application(
    application_id: int,
    data: JobApplicationUpdate,
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

        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can update job applications"
            )

        application = update_job_application(
            db,
            user,
            application_id,
            data
        )

        return application

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


# ==================================================
# DELETE APPLICATION
# ==================================================

@router.delete(
    "/{application_id}",
    status_code=status.HTTP_200_OK
)
def delete_application(
    application_id: int,
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

        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can delete job applications"
            )

        delete_job_application(
            db,
            user,
            application_id
        )

        return {
            "message": "Job application deleted successfully"
        }

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )