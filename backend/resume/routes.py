from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.service import get_user_from_session
from database import get_db
from resume.schemas import (
    ResumeCreate,
    ResumeResponse,
    ResumeUpdate
)
from resume.service import (
    create_resume,
    get_resume,
    update_resume,
    delete_resume
)


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post(
    "",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_resume_route(
    data: ResumeCreate,
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

        # 3. Only students can create resumes
        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can create resumes"
            )

        # 4. Create the resume
        resume = create_resume(
            db,
            user,
            data
        )

        return resume

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Resume already exists"
        )


@router.get(
    "",
    response_model=ResumeResponse,
    status_code=status.HTTP_200_OK
)
def get_resume_route(
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

        # 3. Only students can access resumes
        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can access resumes"
            )

        # 4. Get the student's resume
        resume = get_resume(
            db,
            user
        )

        return resume

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.put(
    "",
    response_model=ResumeResponse,
    status_code=status.HTTP_200_OK
)
def update_resume_route(
    data: ResumeUpdate,
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

        # 3. Only students can update resumes
        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can update resumes"
            )

        # 4. Update the resume
        resume = update_resume(
            db,
            user,
            data
        )

        return resume

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to update resume"
        )


@router.delete(
    "",
    status_code=status.HTTP_200_OK
)
def delete_resume_route(
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

        # 3. Only students can delete resumes
        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can delete resumes"
            )

        # 4. Delete the resume
        delete_resume(
            db,
            user
        )

        return {
            "message": "Resume deleted successfully"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )