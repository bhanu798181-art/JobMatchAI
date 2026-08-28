from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from database import get_db
from external_jobs.models import ExternalJob


router = APIRouter(
    prefix="/external-jobs",
    tags=["External Jobs"]
)


# --------------------------------------------------
# Get external jobs with filters
# --------------------------------------------------

@router.get(
    "",
    status_code=status.HTTP_200_OK
)
def get_external_jobs(
    keyword: str | None = Query(
        default=None
    ),
    location: str | None = Query(
        default=None
    ),
    work_mode: str | None = Query(
        default=None
    ),
    employment_type: str | None = Query(
        default=None
    ),
    source: str | None = Query(
        default=None
    ),
    min_salary: int | None = Query(
        default=None,
        ge=0
    ),
    posted_after: date | None = Query(
        default=None
    ),
    db: Session = Depends(get_db)
):

    query = select(
        ExternalJob
    ).where(
        ExternalJob.status == "active"
    )

    # --------------------------------------------------
    # Keyword filter
    # Searches title, company and description
    # --------------------------------------------------

    if keyword:

        search_text = (
            f"%{keyword.strip()}%"
        )

        query = query.where(
            or_(
                ExternalJob.title.ilike(
                    search_text
                ),
                ExternalJob.company_name.ilike(
                    search_text
                ),
                ExternalJob.description.ilike(
                    search_text
                )
            )
        )

    # --------------------------------------------------
    # Location filter
    # --------------------------------------------------

    if location:

        query = query.where(
            ExternalJob.location.ilike(
                f"%{location.strip()}%"
            )
        )

    # --------------------------------------------------
    # Work mode filter
    # --------------------------------------------------

    if work_mode:

        query = query.where(
            ExternalJob.work_mode.ilike(
                f"%{work_mode.strip()}%"
            )
        )

    # --------------------------------------------------
    # Employment type filter
    # --------------------------------------------------

    if employment_type:

        query = query.where(
            ExternalJob.employment_type.ilike(
                f"%{employment_type.strip()}%"
            )
        )

    # --------------------------------------------------
    # Source filter
    # --------------------------------------------------

    if source:

        query = query.where(
            ExternalJob.source.ilike(
                f"%{source.strip()}%"
            )
        )

    # --------------------------------------------------
    # Minimum salary filter
    # --------------------------------------------------

    if min_salary is not None:

        query = query.where(
            ExternalJob.salary_max >= min_salary
        )

    # --------------------------------------------------
    # Posted-after filter
    # --------------------------------------------------

    if posted_after:

        query = query.where(
            ExternalJob.posted_date >= posted_after
        )

    # --------------------------------------------------
    # Newest jobs first
    # --------------------------------------------------

    query = query.order_by(
        ExternalJob.updated_at.desc()
    )

    jobs = db.scalars(
        query
    ).all()

    return list(jobs)


# --------------------------------------------------
# Get one external job
# --------------------------------------------------

@router.get(
    "/{job_id}",
    status_code=status.HTTP_200_OK
)
def get_external_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    job = db.scalar(
        select(ExternalJob)
        .where(
            ExternalJob.id == job_id,
            ExternalJob.status == "active"
        )
    )

    if not job:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="External job not found"
        )

    return job