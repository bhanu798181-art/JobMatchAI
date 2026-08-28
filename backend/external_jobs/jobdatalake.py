import os
from datetime import datetime, timezone

import requests

from sqlalchemy.orm import Session

from database import engine
from external_jobs.models import ExternalJob


# ==================================================
# CONFIGURATION
# ==================================================

JOBDATALAKE_API_URL = (
    "https://api.jobdatalake.com/v1/jobs"
)

JOBDATALAKE_API_KEY = os.getenv(
    "JOBDATALAKE_API_KEY"
)


# ==================================================
# FETCH JOBS
# ==================================================

def fetch_jobdatalake_jobs(
    keyword: str,
    location: str = "",
    results_per_page: int = 10
) -> list:

    if not JOBDATALAKE_API_KEY:
        raise RuntimeError(
            "JOBDATALAKE_API_KEY is not configured."
        )

    params = {
        "q": keyword,
        "per_page": results_per_page
    }

    if location:
        params["location"] = location

    response = requests.get(
        JOBDATALAKE_API_URL,
        params=params,
        headers={
            "X-API-Key": JOBDATALAKE_API_KEY
        },
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "jobs",
        []
    )


# ==================================================
# CLEAN TEXT
# ==================================================

def clean_text(value):

    if value is None:
        return ""

    return str(value).strip()


# ==================================================
# CONVERT JOB
# ==================================================

def convert_jobdatalake_job(
    job: dict
) -> dict:

    title = clean_text(
        job.get("title")
    )

    company_name = clean_text(
        job.get("company_name")
    )

    locations = job.get(
        "locations",
        []
    )

    # --------------------------------------------------
    # Location
    # --------------------------------------------------

    if isinstance(
        locations,
        list
    ):

        location_parts = []

        for item in locations:

            if isinstance(
                item,
                dict
            ):

                city = clean_text(
                    item.get("city")
                    or item.get(
                        "normalizedCityName"
                    )
                )

                state = clean_text(
                    item.get("state")
                    or item.get(
                        "normalizedStateName"
                    )
                )

                if city and state:

                    location_parts.append(
                        f"{city}, {state}"
                    )

                elif city:

                    location_parts.append(
                        city
                    )

                elif state:

                    location_parts.append(
                        state
                    )

            elif item:

                location_parts.append(
                    clean_text(item)
                )

        location = ", ".join(
            location_parts
        )

    elif isinstance(
        locations,
        dict
    ):

        city = clean_text(
            locations.get("city")
            or locations.get(
                "normalizedCityName"
            )
        )

        state = clean_text(
            locations.get("state")
            or locations.get(
                "normalizedStateName"
            )
        )

        if city and state:

            location = (
                f"{city}, {state}"
            )

        else:

            location = (
                city
                or state
            )

    else:

        location = clean_text(
            locations
        )

    # --------------------------------------------------
    # Safety: database column is VARCHAR(255)
    # --------------------------------------------------

    location = location[:255]

    # --------------------------------------------------
    # Required skills
    # --------------------------------------------------

    required_skills = job.get(
        "required_skills",
        []
    )

    if isinstance(
        required_skills,
        list
    ):

        required_skills = [
            clean_text(skill)
            for skill in required_skills
            if skill
        ]

    else:

        required_skills = []

    # --------------------------------------------------
    # Other fields
    # --------------------------------------------------

    remote_type = clean_text(
        job.get("remote_type")
    )

    employment_type = clean_text(
        job.get("employment_type")
    )

    application_url = clean_text(
        job.get("url")
    )

    external_job_id = clean_text(
        job.get("id")
    )

    # --------------------------------------------------
    # Posted date
    # --------------------------------------------------

    posted_date = None

    posted_at = job.get(
        "posted_at"
    )

    if posted_at:

        try:

            posted_datetime = (
                datetime.fromtimestamp(
                    float(posted_at) / 1000,
                    tz=timezone.utc
                )
            )

            posted_date = (
                posted_datetime.date()
            )

        except (
            ValueError,
            TypeError,
            OverflowError
        ):

            posted_date = None

    # --------------------------------------------------
    # Return converted job
    # --------------------------------------------------

    return {
        "external_job_id": external_job_id,
        "title": title,
        "company_name": company_name,
        "description": None,
        "required_skills": required_skills,
        "location": location,
        "work_mode": remote_type,
        "salary_min": None,
        "salary_max": None,
        "employment_type": employment_type,
        "posted_date": posted_date,
        "application_url": application_url,
        "source": "JobDataLake",
        "source_url": application_url
    }

    # --------------------------------------------------
    # Posted date
    # --------------------------------------------------

    posted_date = None

    posted_at = job.get(
        "posted_at"
    )

    if posted_at:

        try:

            posted_datetime = (
                datetime.fromtimestamp(
                    float(posted_at) / 1000,
                    tz=timezone.utc
                )
            )

            posted_date = (
                posted_datetime.date()
            )

        except (
            ValueError,
            TypeError,
            OverflowError
        ):

            posted_date = None

    return {
        "external_job_id": external_job_id,
        "title": title,
        "company_name": company_name,
        "description": None,
        "required_skills": required_skills,
        "location": location,
        "work_mode": remote_type,
        "salary_min": None,
        "salary_max": None,
        "employment_type": employment_type,
        "posted_date": posted_date,
        "application_url": application_url,
        "source": "JobDataLake",
        "source_url": application_url
    }


# ==================================================
# SAVE JOBS
# ==================================================

def save_jobdatalake_jobs(
    jobs: list
):

    db = Session(
        bind=engine
    )

    saved = 0
    duplicates = 0

    try:

        for raw_job in jobs:

            job_data = (
                convert_jobdatalake_job(
                    raw_job
                )
            )

            external_job_id = (
                job_data[
                    "external_job_id"
                ]
            )

            application_url = (
                job_data[
                    "application_url"
                ]
            )

            # --------------------------------------------------
            # Required fields
            # --------------------------------------------------

            if not external_job_id:
                continue

            if not job_data["title"]:
                continue

            if not job_data["company_name"]:
                continue

            if not application_url:
                continue

            # --------------------------------------------------
            # Find duplicate by source + external ID
            # --------------------------------------------------

            existing_job = (
                db.query(
                    ExternalJob
                )
                .filter(
                    ExternalJob.source
                    == "JobDataLake"
                )
                .filter(
                    ExternalJob.external_job_id
                    == external_job_id
                )
                .first()
            )

            if existing_job:

                duplicates += 1

                continue

            # --------------------------------------------------
            # Create new job
            # --------------------------------------------------

            new_job = ExternalJob(
                title=job_data["title"],
                company_name=(
                    job_data["company_name"]
                ),
                description=(
                    job_data["description"]
                ),
                required_skills=(
                    job_data["required_skills"]
                ),
                location=(
                    job_data["location"]
                ),
                work_mode=(
                    job_data["work_mode"]
                ),
                salary_min=(
                    job_data["salary_min"]
                ),
                salary_max=(
                    job_data["salary_max"]
                ),
                employment_type=(
                    job_data["employment_type"]
                ),
                posted_date=(
                    job_data["posted_date"]
                ),
                application_url=(
                    application_url
                ),
                source="JobDataLake",
                source_url=(
                    job_data["source_url"]
                ),
                external_job_id=(
                    external_job_id
                ),
                status="active"
            )

            db.add(
                new_job
            )

            saved += 1

        db.commit()

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()

    return saved, duplicates