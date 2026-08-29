from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Response,
    status
)

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.schemas import LoginRequest, RegisterRequest

from auth.service import (
    get_user_from_session,
    login_user,
    logout_user,
    register_user
)

from database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# --------------------------------------------------
# REGISTER
# --------------------------------------------------

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    try:

        user = register_user(
            db,
            data
        )

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


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

@router.post(
    "/login",
    status_code=status.HTTP_200_OK
)
def login(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):

    try:

        user, session_token = login_user(
            db,
            data
        )

        # --------------------------------------------------
        # IMPORTANT:
        # Cross-site cookie for Vercel frontend + Render backend
        # --------------------------------------------------

        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=True,
            samesite="none",
            max_age=7 * 24 * 60 * 60,
            path="/"
        )

        return {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role
            }
        }

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )


# --------------------------------------------------
# CURRENT USER
# --------------------------------------------------

@router.get(
    "/me",
    status_code=status.HTTP_200_OK
)
def get_current_user(
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

        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role
            }
        }

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

@router.post(
    "/logout",
    status_code=status.HTTP_200_OK
)
def logout(
    response: Response,
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):

    if session_token:

        logout_user(
            db,
            session_token
        )

    response.delete_cookie(
        key="session_token",
        path="/",
        secure=True,
        samesite="none"
    )

    return {
        "message": "Logout successful"
    }