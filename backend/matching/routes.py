from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.service import get_user_from_session
from database import get_db

from matching.service import get_matching_jobs


router = APIRouter(
    prefix="/matching",
    tags=["Matching"]
)


# ==================================================
# GET MATCHING JOBS
# ==================================================

@router.get(
    "/jobs",
    status_code=status.HTTP_200_OK
)
def get_matching_jobs_route(
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------
    # Check login
    # --------------------------------------------------

    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:

        # --------------------------------------------------
        # Get logged-in user
        # --------------------------------------------------

        user = get_user_from_session(
            db,
            session_token
        )

        # --------------------------------------------------
        # Only students can use job matching
        # --------------------------------------------------

        if user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can access matching jobs"
            )

        # --------------------------------------------------
        # Get matching jobs
        # --------------------------------------------------

        matches = get_matching_jobs(
            db,
            user.id
        )

        return matches

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )