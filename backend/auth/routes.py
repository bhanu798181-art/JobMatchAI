from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.schemas import RegisterRequest
from auth.service import register_user
from database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    try:
        user = register_user(db, data)

        return {
            "message": "Registration successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role
            }
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )