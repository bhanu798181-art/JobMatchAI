from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from models.resume import Resume
from models.user import User
from resume.schemas import (
    ResumeCreate,
    ResumeUpdate
)


def create_resume(
    db: DBSession,
    user: User,
    data: ResumeCreate
) -> Resume:

    # 1. Check whether this user already has a resume
    existing_resume = db.scalar(
        select(Resume).where(
            Resume.user_id == user.id
        )
    )

    if existing_resume:
        raise ValueError("Resume already exists")

    # 2. Create the resume
    resume = Resume(
        user_id=user.id,
        resume_file=data.resume_file,
        resume_text=data.resume_text
    )

    # 3. Add it to the database
    db.add(resume)

    # 4. Save the change
    db.commit()

    # 5. Refresh generated values
    db.refresh(resume)

    return resume


def get_resume(
    db: DBSession,
    user: User
) -> Resume:

    # Find the resume belonging to the logged-in user
    resume = db.scalar(
        select(Resume).where(
            Resume.user_id == user.id
        )
    )

    if not resume:
        raise ValueError("Resume not found")

    return resume


def update_resume(
    db: DBSession,
    user: User,
    data: ResumeUpdate
) -> Resume:

    # 1. Find the resume belonging to the logged-in user
    resume = db.scalar(
        select(Resume).where(
            Resume.user_id == user.id
        )
    )

    # 2. Resume doesn't exist
    if not resume:
        raise ValueError("Resume not found")

    # 3. Get only fields that were actually provided
    update_data = data.model_dump(
        exclude_unset=True
    )

    # 4. Update each provided field
    for field, value in update_data.items():
        setattr(resume, field, value)

    # 5. Save the changes
    db.commit()

    # 6. Refresh the resume
    db.refresh(resume)

    return resume


def delete_resume(
    db: DBSession,
    user: User
) -> None:

    # 1. Find the resume belonging to the logged-in user
    resume = db.scalar(
        select(Resume).where(
            Resume.user_id == user.id
        )
    )

    # 2. Resume doesn't exist
    if not resume:
        raise ValueError("Resume not found")

    # 3. Delete the resume
    db.delete(resume)

    # 4. Save the change
    db.commit()