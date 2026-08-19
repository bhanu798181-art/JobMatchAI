from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.service import get_user_from_session
from applications.schemas import (
    JobApplicationCreate,
    JobApplicationResponse,
    JobApplicationUpdate
)
from applications.service import (
    create_job_application,
    get_job_applications,
    get_job_application,
    update_job_application,
    delete_job_application
)
from database import get_db


router = APIRouter(
    prefix="/applications",
    tags=["Job Applications"]
)


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
    # 1. Check that the user is logged in
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        # 2. Get the authenticated user
        user = get_user_from_session(
            db,
            session_token
        )

        # 3. Only students can create applications
        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can create job applications"
            )

        # 4. Create the application
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


@router.get(
    "",
    response_model=list[JobApplicationResponse],
    status_code=status.HTTP_200_OK
)
def get_applications(
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):
    # 1. Check that the user is logged in
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        # 2. Get the authenticated user
        user = get_user_from_session(
            db,
            session_token
        )

        # 3. Only students can access applications
        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can access job applications"
            )

        # 4. Get all applications belonging to the student
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
    # 1. Check that the user is logged in
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        # 2. Get the authenticated user
        user = get_user_from_session(
            db,
            session_token
        )

        # 3. Only students can access applications
        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can access job applications"
            )

        # 4. Get the requested application
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
    # 1. Check that the user is logged in
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        # 2. Get the authenticated user
        user = get_user_from_session(
            db,
            session_token
        )

        # 3. Only students can update applications
        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can update job applications"
            )

        # 4. Update the application
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


@router.delete(
    "/{application_id}",
    status_code=status.HTTP_200_OK
)
def delete_application(
    application_id: int,
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):
    # 1. Check that the user is logged in
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        # 2. Get the authenticated user
        user = get_user_from_session(
            db,
            session_token
        )

        # 3. Only students can delete applications
        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can delete job applications"
            )

        # 4. Delete the application
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