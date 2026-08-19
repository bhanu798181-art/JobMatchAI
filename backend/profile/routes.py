from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.service import get_user_from_session
from database import get_db
from profile.schemas import (
    StudentProfileCreate,
    StudentProfileResponse,
    StudentProfileUpdate
)
from profile.service import (
    create_student_profile,
    get_student_profile,
    update_student_profile,
    delete_student_profile
)


router = APIRouter(
    prefix="/profile",
    tags=["Student Profile"]
)


@router.post(
    "",
    response_model=StudentProfileResponse,
    status_code=status.HTTP_201_CREATED
)
def create_profile(
    data: StudentProfileCreate,
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
                detail="Only students can create student profiles"
            )

        profile = create_student_profile(
            db,
            user,
            data
        )

        return profile

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student profile already exists"
        )


@router.get(
    "",
    response_model=StudentProfileResponse,
    status_code=status.HTTP_200_OK
)
def get_profile(
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
                detail="Only students can access student profiles"
            )

        profile = get_student_profile(
            db,
            user
        )

        return profile

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.put(
    "",
    response_model=StudentProfileResponse,
    status_code=status.HTTP_200_OK
)
def update_profile(
    data: StudentProfileUpdate,
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
                detail="Only students can update student profiles"
            )

        profile = update_student_profile(
            db,
            user,
            data
        )

        return profile

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to update student profile"
        )


@router.delete(
    "",
    status_code=status.HTTP_200_OK
)
def delete_profile(
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
                detail="Only students can delete student profiles"
            )

        delete_student_profile(
            db,
            user
        )

        return {
            "message": "Student profile deleted successfully"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )