import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from database import SessionLocal
from external_jobs.models import ExternalJob


load_dotenv()


ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api"


# ==================================================
# FETCH JOBS FROM ADZUNA
# ==================================================

def fetch_adzuna_jobs(
    keyword: str = "python developer",
    location: str = "Hyderabad",
    results_per_page: int = 10
):

    if not ADZUNA_APP_ID:
        raise RuntimeError(
            "ADZUNA_APP_ID is not set in .env"
        )

    if not ADZUNA_APP_KEY:
        raise RuntimeError(
            "ADZUNA_APP_KEY is not set in .env"
        )

    url = (
        f"{ADZUNA_BASE_URL}/jobs/in/search/1"
    )

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": keyword,
        "where": location,
        "content-type": "application/json",
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    if response.status_code != 200:

        raise RuntimeError(
            f"Adzuna API request failed: "
            f"{response.status_code} - "
            f"{response.text}"
        )

    data = response.json()

    return data.get(
        "results",
        []
    )


# ==================================================
# SAVE ADZUNA JOBS TO DATABASE
# ==================================================
def save_adzuna_jobs(jobs):

    db = SessionLocal()

    saved = 0
    duplicates = 0

    try:

        for job in jobs:

            external_job_id = str(
                job.get("id")
            )

            # ==================================================
            # BASIC JOB DATA
            # ==================================================

            title = (
                job.get("title")
                or "Untitled Job"
            )

            description = (
                job.get("description")
                or ""
            )


            # ==================================================
            # COMPANY
            # ==================================================

            company = job.get(
                "company",
                {}
            )

            company_name = (
                company.get("display_name")
                or "Unknown Company"
            )


            # ==================================================
            # LOCATION
            # ==================================================

            location_data = job.get(
                "location",
                {}
            )

            job_location = (
                location_data.get("display_name")
                or None
            )


            # ==================================================
            # SALARY
            # ==================================================

            salary_min = job.get(
                "salary_min"
            )

            salary_max = job.get(
                "salary_max"
            )


            # ==================================================
            # EMPLOYMENT TYPE
            # ==================================================

            employment_type = (
                job.get("contract_type")
                or job.get("contract_time")
                or None
            )

            if employment_type:

                employment_type = (
                    str(employment_type)
                    .replace("_", " ")
                    .title()
                )


            # ==================================================
            # POSTED DATE
            # ==================================================

            posted_date = None

            created = job.get(
                "created"
            )

            if created:

                try:

                    posted_date = (
                        datetime.fromisoformat(
                            created.replace(
                                "Z",
                                "+00:00"
                            )
                        ).date()
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    posted_date = None


            # ==================================================
            # WORK MODE
            # ==================================================

            text_for_work_mode = (
                f"{title} {description}"
            ).lower()

            if "remote" in text_for_work_mode:

                work_mode = "Remote"

            elif "work from home" in text_for_work_mode:

                work_mode = "Remote"

            elif "hybrid" in text_for_work_mode:

                work_mode = "Hybrid"

            else:

                work_mode = "On-site"


            # ==================================================
            # REQUIRED SKILLS
            # ==================================================

            required_skills = []

            skill_keywords = [

                "python",
                "java",
                "javascript",
                "typescript",

                "react",
                "node.js",
                "node",

                "c",
                "c++",
                "c#",

                "sql",
                "mysql",
                "postgresql",

                "html",
                "css",

                "php",

                "angular",
                "vue",

                "django",
                "flask",
                "spring",
                "spring boot",

                "aws",
                "azure",
                "gcp",

                "docker",
                "kubernetes",

                "git",
                "github",

                "machine learning",
                "deep learning",
                "data analysis",

                "excel",

                "power bi",
                "tableau"
            ]

            text_for_skills = (
                f"{title} {description}"
            ).lower()

            for skill in skill_keywords:

                if skill.lower() in text_for_skills:

                    if skill not in required_skills:

                        required_skills.append(
                            skill
                        )

            if not required_skills:

                required_skills = None


            # ==================================================
            # CHECK DUPLICATE
            # ==================================================

            existing_job = (
                db.query(ExternalJob)
                .filter(
                    ExternalJob.source == "Adzuna",
                    ExternalJob.external_job_id
                    == external_job_id
                )
                .first()
            )


            # ==================================================
            # UPDATE EXISTING JOB
            # ==================================================

            if existing_job:

                duplicates += 1

                existing_job.title = title

                existing_job.company_name = (
                    company_name
                )

                existing_job.description = (
                    description
                )

                existing_job.required_skills = (
                    required_skills
                )

                existing_job.location = (
                    job_location
                )

                existing_job.work_mode = (
                    work_mode
                )

                existing_job.salary_min = (
                    salary_min
                )

                existing_job.salary_max = (
                    salary_max
                )

                existing_job.employment_type = (
                    employment_type
                )

                existing_job.posted_date = (
                    posted_date
                )

                existing_job.application_url = (
                    job.get("redirect_url")
                    or existing_job.application_url
                )

                existing_job.status = "active"

                continue


            # ==================================================
            # CREATE NEW JOB
            # ==================================================

            new_job = ExternalJob(

                title=title,

                company_name=company_name,

                description=description,

                required_skills=required_skills,

                location=job_location,

                work_mode=work_mode,

                salary_min=salary_min,

                salary_max=salary_max,

                employment_type=employment_type,

                posted_date=posted_date,

                application_url=(
                    job.get("redirect_url")
                    or ""
                ),

                source="Adzuna",

                source_url=(
                    "https://www.adzuna.com/"
                ),

                external_job_id=(
                    external_job_id
                ),

                status="active"
            )

            db.add(new_job)

            saved += 1


        # ==================================================
        # COMMIT
        # ==================================================

        db.commit()

        return (
            saved,
            duplicates
        )


    except Exception:

        db.rollback()

        raise


    finally:

        db.close()
# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    print("=" * 60)
    print("JOBMATCH AI - ADZUNA JOB COLLECTION")
    print("=" * 60)

    try:

        jobs = fetch_adzuna_jobs()

        print(
            f"Jobs received: {len(jobs)}"
        )

        saved, duplicates = (
            save_adzuna_jobs(
                jobs
            )
        )

        print(
            f"New jobs saved: {saved}"
        )

        print(
            f"Duplicates found: {duplicates}"
        )

        print("=" * 60)
        print("ADZUNA COLLECTION COMPLETED")
        print("=" * 60)

    except Exception as error:

        print("=" * 60)
        print("ADZUNA COLLECTION FAILED")
        print("=" * 60)

        print(
            f"Error: {error}"
        )