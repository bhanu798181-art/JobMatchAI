from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.service import get_user_from_session
from database import get_db
from preferences.schemas import (
    JobPreferenceCreate,
    JobPreferenceResponse,
    JobPreferenceUpdate
)
from preferences.service import (
    create_job_preference,
    get_job_preference,
    update_job_preference,
    delete_job_preference
)


router = APIRouter(
    prefix="/preferences",
    tags=["Job Preferences"]
)


@router.post(
    "",
    response_model=JobPreferenceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_preference(
    data: JobPreferenceCreate,
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

        # 3. Only students can create job preferences
        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can create job preferences"
            )

        # 4. Create the job preference
        preference = create_job_preference(
            db,
            user,
            data
        )

        return preference

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Job preference already exists"
        )


@router.get(
    "",
    response_model=JobPreferenceResponse,
    status_code=status.HTTP_200_OK
)
def get_preference(
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

        # 3. Only students can access job preferences
        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can access job preferences"
            )

        # 4. Get the student's job preference
        preference = get_job_preference(
            db,
            user
        )

        return preference

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.put(
    "",
    response_model=JobPreferenceResponse,
    status_code=status.HTTP_200_OK
)
def update_preference(
    data: JobPreferenceUpdate,
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

        # 3. Only students can update job preferences
        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can update job preferences"
            )

        # 4. Update the job preference
        preference = update_job_preference(
            db,
            user,
            data
        )

        return preference

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to update job preference"
        )


@router.delete(
    "",
    status_code=status.HTTP_200_OK
)
def delete_preference(
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

        # 3. Only students can delete job preferences
        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can delete job preferences"
            )

        # 4. Delete the job preference
        delete_job_preference(
            db,
            user
        )

        return {
            "message": "Job preference deleted successfully"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )