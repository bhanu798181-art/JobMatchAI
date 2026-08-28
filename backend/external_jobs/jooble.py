import os
import sys
import re
from datetime import datetime, date

import requests
from dotenv import load_dotenv

# --------------------------------------------------
# Make backend imports work
# --------------------------------------------------

BACKEND_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv(
    os.path.join(
        BACKEND_DIR,
        ".env"
    )
)


# --------------------------------------------------
# Database imports
# --------------------------------------------------

from database import SessionLocal
from external_jobs.models import ExternalJob


# --------------------------------------------------
# Jooble configuration
# --------------------------------------------------

JOOBLE_API_KEY = os.getenv(
    "JOOBLE_API_KEY"
)

JOOBLE_BASE_URL = (
    "https://in.jooble.org/api"
)


# ==================================================
# TEXT CLEANING
# ==================================================

def clean_text(value):
    if not value:
        return ""

    text = str(value)

    # Remove HTML tags
    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    # Decode HTML entities
    import html

    text = html.unescape(text)

    # Remove common markdown formatting
    text = re.sub(
        r"#{1,6}\s*",
        "",
        text
    )

    # Replace bullets with readable separators
    text = text.replace(
        "•",
        " • "
    )

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==================================================
# SKILL MASTER LIST
# ==================================================

def get_skill_master_list():

    from sqlalchemy import text

    db = SessionLocal()

    try:

        result = db.execute(
            text(
                """
                SELECT canonical_name
                FROM skills_master
                ORDER BY id
                """
            )
        )

        skill_names = []

        for row in result:

            if not row[0]:
                continue

            name = str(
                row[0]
            ).strip()

            if name:

                skill_names.append(
                    name
                )

        return skill_names

    finally:

        db.close()


# ==================================================
# DETECT REQUIRED SKILLS
# ==================================================

def detect_required_skills(
    title,
    description
):

    title_text = clean_text(
        title
    )

    description_text = clean_text(
        description
    )

    searchable_text = (
        f"{title_text} {description_text}"
    ).lower()

    try:

        skill_names = (
            get_skill_master_list()
        )

    except Exception as error:

        print(
            "Skill master lookup failed:",
            error
        )

        return []

    detected_skills = []

    for skill_name in skill_names:

        skill_lower = (
            skill_name.lower().strip()
        )

        if not skill_lower:
            continue

        escaped_skill = re.escape(
            skill_lower
        )

        pattern = (
            rf"(?<![a-z0-9])"
            rf"{escaped_skill}"
            rf"(?![a-z0-9])"
        )

        if re.search(
            pattern,
            searchable_text,
            re.IGNORECASE
        ):

            detected_skills.append(
                skill_name
            )

    return detected_skills


# ==================================================
# DETECT WORK MODE
# ==================================================

def detect_work_mode(
    title,
    description
):

    text = (
        f"{clean_text(title)} "
        f"{clean_text(description)}"
    ).lower()

    # ==================================================
    # HYBRID
    # Check this FIRST because hybrid jobs can also
    # mention office/on-site and work-from-home.
    # ==================================================

    hybrid_patterns = [
        r"\bhybrid\b",
        r"\bhybrid work\b",
        r"\bhybrid working\b",
        r"\bhybrid model\b",
        r"\bhybrid after\b",
        r"\bwfo\b.*\bwfh\b",
        r"\bwfh\b.*\bwfo\b",
        r"\bwork from office\b.*\bwork from home\b",
        r"\bwork from home\b.*\bwork from office\b",
    ]

    for pattern in hybrid_patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            return "Hybrid"

    # ==================================================
    # REMOTE
    # ==================================================

    remote_patterns = [
        r"\bfully remote\b",
        r"\bremote position\b",
        r"\bremote working\b",
        r"\bwork from home\b",
        r"\bwfh\b",
        r"\bremote\b",
    ]

    for pattern in remote_patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            return "Remote"

    # ==================================================
    # ON-SITE
    # ==================================================

    onsite_patterns = [
        r"\bon[- ]?site\b",
        r"\bonsite\b",
        r"\boffice[- ]based\b",
        r"\bwork from office\b",
        r"\bwfo\b",
        r"\bin office\b",
    ]

    for pattern in onsite_patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            return "On-site"

    return None


# ==================================================
# DETECT EMPLOYMENT TYPE
# ==================================================

def detect_employment_type(
    title,
    description
):

    text = (
        f"{clean_text(title)} "
        f"{clean_text(description)}"
    )

    # Normalize everything
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    text_lower = text.lower()

    # ==================================================
    # INTERNSHIP
    # ==================================================

    internship_patterns = [
        r"\binternship\b",
        r"\bintern\b",
        r"\btrainee\b",
        r"\bapprentice\b",
        r"\bjob\s*type\s*[:\-]?\s*internship\b",
    ]

    for pattern in internship_patterns:

        if re.search(
            pattern,
            text_lower
        ):
            return "Internship"

    # ==================================================
    # PART-TIME
    # ==================================================

    part_time_patterns = [
        r"\bpart[-\s]?time\b",
        r"\bparttime\b",
        r"\bjob\s*type\s*[:\-]?\s*part[-\s]?time\b",
    ]

    for pattern in part_time_patterns:

        if re.search(
            pattern,
            text_lower
        ):
            return "Part-time"

    # ==================================================
    # CONTRACT
    # ==================================================

    contract_patterns = [
        r"\bcontract(?:ual)?\b",
        r"\bcontractor\b",
        r"\bjob\s*type\s*[:\-]?\s*contract\b",
    ]

    for pattern in contract_patterns:

        if re.search(
            pattern,
            text_lower
        ):
            return "Contract"

    # ==================================================
    # FREELANCE
    # ==================================================

    freelance_patterns = [
        r"\bfreelance\b",
        r"\bfreelancer\b",
        r"\bjob\s*type\s*[:\-]?\s*freelance\b",
    ]

    for pattern in freelance_patterns:

        if re.search(
            pattern,
            text_lower
        ):
            return "Freelance"

        # ==================================================
    # FULL-TIME
    # ==================================================

    full_time_patterns = [
        r"\bfull[-\s]?time\b",
        r"\bfulltime\b",
        r"\bpermanent\b",
        r"\bregular employment\b",
        r"job\s*type\s*[:\-]?\s*full[-\s]?time",
    ]

    for pattern in full_time_patterns:

        if re.search(
            pattern,
            text_lower
        ):
            return "Full-time"

    # Jooble sometimes joins the next word directly
    # Example: "Full-TimeExperience"
    if re.search(
        r"full[-\s]?time",
        text_lower
    ):
        return "Full-time"

    return None


# ==================================================
# DETECT SALARY
# ==================================================

def detect_salary(
    title,
    description
):

    text = (
        f"{clean_text(title)} "
        f"{clean_text(description)}"
    )

    text_lower = text.lower()

    salary_min = None
    salary_max = None

    # --------------------------------------------------
    # Indian LPA format
    # Examples:
    # 3 LPA
    # 3-6 LPA
    # 5 to 8 LPA
    # ₹3 LPA
    # ₹3-6 LPA
    # --------------------------------------------------

    lpa_range_pattern = re.search(
        r"(?:₹|rs\.?|inr)?\s*"
        r"(\d+(?:\.\d+)?)"
        r"\s*(?:-|to)\s*"
        r"(\d+(?:\.\d+)?)"
        r"\s*(?:lpa|lakhs?|lac)",
        text_lower,
        re.IGNORECASE
    )

    if lpa_range_pattern:

        salary_min = (
            float(lpa_range_pattern.group(1))
            * 100000
        )

        salary_max = (
            float(lpa_range_pattern.group(2))
            * 100000
        )

        return (
            int(salary_min),
            int(salary_max)
        )

    # --------------------------------------------------
    # Single LPA value
    # --------------------------------------------------

    lpa_single_pattern = re.search(
        r"(?:₹|rs\.?|inr)?\s*"
        r"(\d+(?:\.\d+)?)"
        r"\s*(?:lpa|lakhs?|lac)",
        text_lower,
        re.IGNORECASE
    )

    if lpa_single_pattern:

        salary = (
            float(
                lpa_single_pattern.group(1)
            )
            * 100000
        )

        return (
            int(salary),
            int(salary)
        )

    # --------------------------------------------------
    # Thousand / K format
    # Examples:
    # 30K - 50K
    # 30000 - 50000
    # --------------------------------------------------

    k_range_pattern = re.search(
        r"(?:₹|rs\.?|inr)?\s*"
        r"(\d+(?:\.\d+)?)\s*k"
        r"\s*(?:-|to)\s*"
        r"(\d+(?:\.\d+)?)\s*k",
        text_lower,
        re.IGNORECASE
    )

    if k_range_pattern:

        salary_min = (
            float(k_range_pattern.group(1))
            * 1000
        )

        salary_max = (
            float(k_range_pattern.group(2))
            * 1000
        )

        return (
            int(salary_min),
            int(salary_max)
        )

    # --------------------------------------------------
    # Plain INR range
    # --------------------------------------------------

    inr_range_pattern = re.search(
        r"(?:₹|rs\.?|inr)\s*"
        r"([\d,]+)"
        r"\s*(?:-|to)\s*"
        r"(?:₹|rs\.?|inr)?\s*"
        r"([\d,]+)",
        text_lower,
        re.IGNORECASE
    )

    if inr_range_pattern:

        salary_min = int(
            inr_range_pattern
            .group(1)
            .replace(",", "")
        )

        salary_max = int(
            inr_range_pattern
            .group(2)
            .replace(",", "")
        )

        return (
            salary_min,
            salary_max
        )

    return (
        None,
        None
    )


# ==================================================
# PARSE JOOBLE DATE
# ==================================================

def parse_date(value):

    if not value:
        return None

    if isinstance(
        value,
        date
    ):

        return value

    value = str(
        value
    ).strip()

    if not value:
        return None

    # ISO format
    try:

        return datetime.fromisoformat(
            value.replace(
                "Z",
                "+00:00"
            )
        ).date()

    except (
        ValueError,
        TypeError
    ):

        pass

    # Common date formats
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
    ]

    for fmt in formats:

        try:

            return datetime.strptime(
                value,
                fmt
            ).date()

        except ValueError:

            continue

    return None


# ==================================================
# FETCH JOBS FROM JOOBLE
# ==================================================

def fetch_jooble_jobs(
    keyword: str = "python developer",
    location: str = "Hyderabad",
    results_per_page: int = 10
):

    if not JOOBLE_API_KEY:

        raise RuntimeError(
            "JOOBLE_API_KEY is not set in .env"
        )

    url = (
        f"{JOOBLE_BASE_URL}/"
        f"{JOOBLE_API_KEY}"
    )

    payload = {

        "keywords": keyword,

        "location": location,

        "page": "1",

        "ResultOnPage": results_per_page,

        "companysearch": "false"
    }

    response = requests.post(
        url,
        json=payload,
        headers={
            "Content-Type": "application/json"
        },
        timeout=30
    )

    print(
        "Jooble status:",
        response.status_code
    )

    if response.status_code != 200:

        raise RuntimeError(
            "Jooble API request failed: "
            f"{response.status_code} - "
            f"{response.text}"
        )

    data = response.json()

    jobs = data.get(
        "jobs",
        []
    )

    return jobs


# ==================================================
# SAVE JOOBLE JOBS
# ==================================================

def save_jooble_jobs(
    jobs
):

    db = SessionLocal()

    saved_count = 0
    duplicate_count = 0

    try:

        for job in jobs:

            # --------------------------------------------------
            # Basic information
            # --------------------------------------------------

            external_job_id = (

                str(
                    job.get("id")
                )

                if job.get("id") is not None

                else None
            )

            application_url = (
                job.get("link")
            )

            company_name = (
                job.get("company")
                or "Unknown Company"
            )

            title = (
                job.get("title")
                or "Untitled Job"
            )

            location = (
                job.get("location")
            )

            description = (
                job.get("description")
                or job.get("snippet")
                or ""
            )

            # Clean text
            title = clean_text(
                title
            )

            company_name = clean_text(
                company_name
            )

            location = clean_text(
                location
            )

            description = clean_text(
                description
            )

            # --------------------------------------------------
            # Detect skills
            # --------------------------------------------------

            required_skills = (
                detect_required_skills(
                    title,
                    description
                )
            )

            # --------------------------------------------------
            # Detect work mode
            # --------------------------------------------------

            work_mode = (
                detect_work_mode(
                    title,
                    description
                )
            )

            # --------------------------------------------------
            # Detect employment type
            # --------------------------------------------------

            employment_type = (
                detect_employment_type(
                    title,
                    description
                )
            )

            # --------------------------------------------------
            # Detect salary
            # --------------------------------------------------

            salary_min, salary_max = (
                detect_salary(
                    title,
                    description
                )
            )

            # --------------------------------------------------
            # Posted date
            # --------------------------------------------------

            posted_date = parse_date(
                job.get("updated")
            )


            # --------------------------------------------------
            # Find duplicate by Jooble ID
            # --------------------------------------------------

            existing_job = None

            if external_job_id:

                existing_job = (
                    db.query(
                        ExternalJob
                    )
                    .filter(
                        ExternalJob.source
                        == "Jooble",

                        ExternalJob.external_job_id
                        == external_job_id
                    )
                    .first()
                )

            # --------------------------------------------------
            # Find duplicate by application URL
            # --------------------------------------------------

            if (
                not existing_job
                and application_url
            ):

                existing_job = (
                    db.query(
                        ExternalJob
                    )
                    .filter(
                        ExternalJob.application_url
                        == application_url
                    )
                    .first()
                )

            # --------------------------------------------------
            # Existing job
            # --------------------------------------------------

            if existing_job:

                duplicate_count += 1

                existing_job.title = title

                existing_job.company_name = (
                    company_name
                )

                existing_job.description = (
                    description
                )

                existing_job.location = (
                    location
                    or existing_job.location
                )

                # Update only when detected
                if required_skills:

                    existing_job.required_skills = (
                        required_skills
                    )

                if work_mode:

                    existing_job.work_mode = (
                        work_mode
                    )

                if employment_type:

                    existing_job.employment_type = (
                        employment_type
                    )

                if salary_min is not None:

                    existing_job.salary_min = (
                        salary_min
                    )

                if salary_max is not None:

                    existing_job.salary_max = (
                        salary_max
                    )

                if posted_date:

                    existing_job.posted_date = (
                        posted_date
                    )

                if application_url:

                    existing_job.application_url = (
                        application_url
                    )

                existing_job.status = (
                    "active"
                )

                existing_job.updated_at = (
                    datetime.now()
                )

                continue

            # --------------------------------------------------
            # New job
            # --------------------------------------------------

            new_job = ExternalJob(

                title=title,

                company_name=company_name,

                description=description,

                required_skills=(
                    required_skills
                    if required_skills
                    else None
                ),

                location=(
                    location
                    or None
                ),

                work_mode=work_mode,

                salary_min=salary_min,

                salary_max=salary_max,

                employment_type=employment_type,

                posted_date=posted_date,

                application_url=(
                    application_url
                    or "https://in.jooble.org/"
                ),

                source="Jooble",

                source_url=(
                    job.get("source")
                    or "https://in.jooble.org/"
                ),

                external_job_id=(
                    external_job_id
                ),

                status="active"
            )

            db.add(
                new_job
            )

            saved_count += 1

        # --------------------------------------------------
        # Commit
        # --------------------------------------------------

        db.commit()

        return (
            saved_count,
            duplicate_count
        )

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


# ==================================================
# MAIN TEST
# ==================================================

if __name__ == "__main__":

    print("=" * 60)

    print(
        "JOBMATCH AI - JOOBLE JOB COLLECTION"
    )

    print("=" * 60)

    print()

    print(
        "Fetching jobs from Jooble..."
    )

    jobs = fetch_jooble_jobs()

    print()

    print(
        f"Jobs received: {len(jobs)}"
    )

    print()

    print(
        "Saving jobs to PostgreSQL..."
    )

    saved, duplicates = (
        save_jooble_jobs(
            jobs
        )
    )

    print()

    print(
        "-" * 60
    )

    print(
        f"New jobs saved: {saved}"
    )

    print(
        f"Duplicates found: {duplicates}"
    )

    print(
        "Jooble import completed."
    )

    print("=" * 60)
