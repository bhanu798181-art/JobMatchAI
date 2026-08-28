from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.service import get_user_from_session
from database import get_db

from profile.service import (
    create_student_profile,
    get_student_profile,
    update_student_profile,
    delete_student_profile,
    get_all_skills,
    get_student_skills,
    add_student_skill,
    remove_student_skill,
    get_student_education,
    update_student_education
)

from profile.schemas import (
    StudentProfileCreate,
    StudentProfileResponse,
    StudentProfileUpdate,
    SkillResponse,
    StudentSkillResponse,
    StudentSkillAdd,
    EducationResponse,
    EducationUpdate
)


router = APIRouter(
    prefix="/profile",
    tags=["Student Profile"]
)


# ==================================================
# CREATE STUDENT PROFILE
# ==================================================

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

        return create_student_profile(
            db,
            user,
            data
        )

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


# ==================================================
# GET STUDENT PROFILE
# ==================================================

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

        return get_student_profile(
            db,
            user
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


# ==================================================
# UPDATE STUDENT PROFILE
# ==================================================

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

        return update_student_profile(
            db,
            user,
            data
        )

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


# ==================================================
# DELETE STUDENT PROFILE
# ==================================================

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


# ==================================================
# GET ALL AVAILABLE SKILLS
# ==================================================

@router.get(
    "/skills/all",
    response_model=list[SkillResponse],
    status_code=status.HTTP_200_OK
)
def get_skills(
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
                detail="Only students can access skills"
            )

        return get_all_skills(db)

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


# ==================================================
# GET STUDENT SKILLS
# ==================================================

@router.get(
    "/skills",
    response_model=list[StudentSkillResponse],
    status_code=status.HTTP_200_OK
)
def get_my_skills(
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
                detail="Only students can access skills"
            )

        return get_student_skills(
            db,
            user
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


# ==================================================
# ADD STUDENT SKILL
# ==================================================

@router.post(
    "/skills",
    response_model=StudentSkillResponse,
    status_code=status.HTTP_200_OK
)
def add_skill(
    data: StudentSkillAdd,
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
                detail="Only students can manage skills"
            )

        return add_student_skill(
            db,
            user,
            data.skill_id,
            data.proficiency
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to add skill"
        )


# ==================================================
# DELETE STUDENT SKILL
# ==================================================

@router.delete(
    "/skills/{skill_id}",
    status_code=status.HTTP_200_OK
)
def remove_skill(
    skill_id: int,
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
                detail="Only students can manage skills"
            )

        remove_student_skill(
            db,
            user,
            skill_id
        )

        return {
            "message": "Skill removed successfully"
        }

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
# ==================================================
# GET STUDENT EDUCATION
# ==================================================

@router.get(
    "/education",
    response_model=list[EducationResponse],
    status_code=status.HTTP_200_OK
)
def get_my_education(
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
                detail="Only students can access education"
            )

        return get_student_education(
            db,
            user
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
    # ==================================================
# UPDATE STUDENT EDUCATION
# ==================================================

@router.put(
    "/education/{education_id}",
    response_model=EducationResponse,
    status_code=status.HTTP_200_OK
)
def update_my_education(
    education_id: int,
    data: EducationUpdate,
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
                detail="Only students can update education"
            )

        return update_student_education(
            db,
            user,
            education_id,
            data
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )