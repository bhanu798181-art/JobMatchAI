import re

from sqlalchemy import select

from sqlalchemy.orm import Session as DBSession

from models.education import Education
from models.experience import Experience
from models.job import Job
from models.preference import Preference
from models.student_profile import StudentProfile
from models.student_skill import StudentSkill
from models.skill_master import SkillMaster

from external_jobs.models import ExternalJob


# ==================================================
# GET STUDENT DATA
# ==================================================

def get_student_data(
    db: DBSession,
    user_id: int
):
    student = db.scalar(
        select(StudentProfile).where(
            StudentProfile.user_id == user_id
        )
    )

    if not student:
        raise ValueError(
            "Student profile not found"
        )

    education = db.scalars(
        select(Education).where(
            Education.student_id == student.id
        )
    ).all()

    skills = db.execute(
        select(StudentSkill, SkillMaster)
        .join(
            SkillMaster,
            StudentSkill.skill_id == SkillMaster.id
        )
        .where(
            StudentSkill.student_id == student.id
        )
    ).all()

    experiences = db.scalars(
        select(Experience).where(
            Experience.student_id == student.id
        )
    ).all()

    preference = db.scalar(
        select(Preference).where(
            Preference.student_id == student.id
        )
    )

    return {
        "student": student,
        "education": list(education),
        "skills": list(skills),
        "experiences": list(experiences),
        "preference": preference
    }


# ==================================================
# NORMALIZE SKILL NAME
# ==================================================

def normalize_skill_name(
    skill_name: str
) -> str:

    if not skill_name:
        return ""

    name = (
        str(skill_name)
        .lower()
        .strip()
    )

    # Normalize common punctuation
    name = (
        name
        .replace("-", " ")
        .replace("_", " ")
        .replace(".", " ")
        .replace("/", " ")
    )

    # Remove extra spaces
    name = " ".join(
        name.split()
    )

    aliases = {

        # ------------------------------------------
        # Programming languages
        # ------------------------------------------

        "py": "python",
        "python programming": "python",
        "python development": "python",

        "js": "javascript",
        "javascript programming": "javascript",
        "javascript development": "javascript",

        "ts": "typescript",
        "typescript programming": "typescript",

        "java programming": "java",
        "java development": "java",

        "c programming": "c",
        "cpp": "c++",
        "c plus plus": "c++",

# ------------------------------------------
# Web
# ------------------------------------------

"html5": "html",
"css3": "css",

"fast api": "fastapi",
"fastapi": "fastapi",

        "reactjs": "react",
        "react js": "react",
        "react javascript": "react",

        "nodejs": "node",
        "node js": "node",

        "expressjs": "express",
        "express js": "express",

        # ------------------------------------------
        # Databases
        # ------------------------------------------

        "postgres": "postgresql",
        "postgre sql": "postgresql",

        "mongo": "mongodb",

        "structured query language": "sql",

        # ------------------------------------------
        # Tools
        # ------------------------------------------

        "git version control": "git",

        # ------------------------------------------
        # AI / ML
        # ------------------------------------------

        "ml": "machine learning",
        "machine learning": "machine learning",

        "ai": "artificial intelligence",
        "artificial intelligence": "artificial intelligence",

        # ------------------------------------------
        # Cloud
        # ------------------------------------------

        "amazon web services": "aws",

        "google cloud platform": "gcp",

        "microsoft azure": "azure",

        # ------------------------------------------
        # Data
        # ------------------------------------------

        "data analysis": "data analyst",
        "data analytics": "data analyst",

        # ------------------------------------------
        # Other common skills
        # ------------------------------------------

        "rest api": "rest",
        "rest apis": "rest",

        "restful api": "rest",
        "restful apis": "rest",

        "docker container": "docker",
        "docker containers": "docker",
    }

    return aliases.get(
        name,
        name
    )


# ==================================================
# GET STUDENT SKILL NAMES
# ==================================================

def get_student_skill_names(
    student_data: dict
):

    skill_names = set()

    for student_skill, skill_master in (
        student_data["skills"]
    ):

        if not skill_master:
            continue

        skill_name = (
            skill_master.canonical_name
            or getattr(
                skill_master,
                "name",
                None
            )
        )

        if skill_name:

            normalized_name = (
                normalize_skill_name(
                    skill_name
                )
            )

            if normalized_name:
                skill_names.add(
                    normalized_name
                )

    return skill_names


# ==================================================
# COMMON SKILLS WE CAN DETECT FROM EXTERNAL JOB TEXT
# ==================================================

COMMON_SKILLS = [

    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",

    "html",
    "css",
    "react",
    "angular",
    "vue",

    "node",
    "express",

    "sql",
    "mysql",
    "postgresql",
    "mongodb",

    "git",
    "github",
    "docker",
    "kubernetes",

    "aws",
    "azure",
    "gcp",

    "fastapi",
    "django",
    "flask",

    "spring",
    "spring boot",

    "rest",

    "machine learning",
    "artificial intelligence",

    "pandas",
    "numpy",

    "data analyst",
    "data analysis",

    "power bi",
    "tableau",

    "excel",

    "linux",
]


# ==================================================
# DETECT SKILLS FROM JOB TEXT
# ==================================================

def detect_skills_from_text(
    text: str
) -> list[str]:

    if not text:
        return []

    normalized_text = (
        str(text)
        .lower()
        .replace("-", " ")
        .replace("_", " ")
        .replace("/", " ")
    )

    # Remove HTML tags and normalize whitespace
    normalized_text = re.sub(
        r"<[^>]+>",
        " ",
        normalized_text
    )

    normalized_text = re.sub(
        r"\s+",
        " ",
        normalized_text
    ).strip()

    detected = []

    for skill in COMMON_SKILLS:

        normalized_skill = (
            normalize_skill_name(
                skill
            )
        )

        if not normalized_skill:
            continue

        # --------------------------------------------------
        # Skill aliases / alternate spellings
        # --------------------------------------------------

        search_variants = [
            normalized_skill
        ]

        if normalized_skill == "fastapi":

            search_variants.append(
                "fast api"
            )

        elif normalized_skill == "postgresql":

            search_variants.append(
                "postgre sql"
            )

        elif normalized_skill == "javascript":

            search_variants.append(
                "java script"
            )

        elif normalized_skill == "typescript":

            search_variants.append(
                "type script"
            )

        # --------------------------------------------------
        # Whole word / phrase matching
        #
        # Prevents:
        #
        # "c" matching "candidate"
        # "java" matching "javascript"
        # etc.
        # --------------------------------------------------

        for search_skill in search_variants:

            pattern = (
                r"(?<!\w)"
                + re.escape(search_skill)
                + r"(?!\w)"
            )

            if re.search(
                pattern,
                normalized_text
            ):

                if (
                    normalized_skill
                    not in detected
                ):

                    detected.append(
                        normalized_skill
                    )

                break

    return detected

# ==================================================
# DETECT EXTERNAL JOB SKILLS
# ==================================================

def get_external_job_skills(
    job: ExternalJob
) -> list[str]:

    detected_skills = []

    # ------------------------------------------
    # 1. Skills already provided by source
    # ------------------------------------------

    for skill in (
        job.required_skills or []
    ):

        normalized = (
            normalize_skill_name(
                skill
            )
        )

        if (
            normalized
            and normalized not in detected_skills
        ):

            detected_skills.append(
                normalized
            )

    # ------------------------------------------
    # 2. Detect skills from title
    # ------------------------------------------

    title_skills = (
        detect_skills_from_text(
            job.title or ""
        )
    )

    for skill in title_skills:

        if skill not in detected_skills:

            detected_skills.append(
                skill
            )

    # ------------------------------------------
    # 3. Detect skills from description
    # ------------------------------------------

    description_skills = (
        detect_skills_from_text(
            job.description or ""
        )
    )

    for skill in description_skills:

        if skill not in detected_skills:

            detected_skills.append(
                skill
            )

    return detected_skills


# ==================================================
# CHECK TEXT FOR STUDENT SKILL
# ==================================================

def text_contains_skill(
    text: str,
    student_skill: str
) -> bool:

    if not text or not student_skill:
        return False

    normalized_text = (
        text.lower()
        .replace("-", " ")
        .replace("_", " ")
        .replace("/", " ")
    )

    normalized_skill = (
        normalize_skill_name(
            student_skill
        )
    )

    if not normalized_skill:
        return False

    return normalized_skill in normalized_text


# ==================================================
# MATCH INTERNAL JOB
# ==================================================

def calculate_job_match(
    job: Job,
    student_data: dict
) -> dict:

    education_list = (
        student_data["education"]
    )

    experiences = (
        student_data["experiences"]
    )

    preference = (
        student_data["preference"]
    )

    student_skill_names = (
        get_student_skill_names(
            student_data
        )
    )

    score = 0
    reasons = []

    # ==================================================
    # 1. Education - 15 points
    # ==================================================

    education_score = 0

    for education in education_list:

        qualification = (
            education.qualification
            or ""
        ).lower()

        requirement = (
            job.education_requirement
            or ""
        ).lower()

        if (
            qualification
            and requirement
            and qualification in requirement
        ):

            education_score = 15

            reasons.append(
                "Education requirement matches"
            )

            break

        if (
            job.education_accepts_diploma
            and qualification == "diploma"
        ):

            education_score = 15

            reasons.append(
                "Diploma is accepted"
            )

            break

    score += education_score

    # ==================================================
    # 2. Branch - 15 points
    # ==================================================

    branch_score = 0

    if job.branch_requirement:

        for education in education_list:

            if not education.branch:
                continue

            student_branch = (
                education.branch
                .lower()
                .strip()
            )

            for required_branch in (
                job.branch_requirement
            ):

                if (
                    required_branch
                    and required_branch.lower().strip()
                    == student_branch
                ):

                    branch_score = 15

                    reasons.append(
                        "Branch requirement matches"
                    )

                    break

            if branch_score:
                break

    else:

        branch_score = 15

        reasons.append(
            "No specific branch restriction"
        )

    score += branch_score

    # ==================================================
    # 3. Academic - 10 points
    # ==================================================

    academic_score = 0

    for education in education_list:

        if (
            job.min_cgpa is not None
            and education.cgpa is not None
            and float(education.cgpa)
            >= float(job.min_cgpa)
        ):

            academic_score = 10

            reasons.append(
                "CGPA requirement satisfied"
            )

            break

        if (
            job.min_percentage is not None
            and education.percentage is not None
            and float(education.percentage)
            >= float(job.min_percentage)
        ):

            academic_score = 10

            reasons.append(
                "Percentage requirement satisfied"
            )

            break

    score += academic_score

    # ==================================================
    # 4. Experience - 10 points
    # ==================================================

    experience_score = 0

    if not job.experience_requirement:

        experience_score = 10

        reasons.append(
            "No specific experience requirement"
        )

    elif experiences:

        experience_score = 10

        reasons.append(
            "Relevant experience available"
        )

    elif (
        job.experience_requirement
        .lower()
        .strip()
        == "fresher"
    ):

        experience_score = 10

        reasons.append(
            "Fresher position"
        )

    score += experience_score

    # ==================================================
    # 5. Location - 10 points
    # ==================================================

    location_score = 0

    student_city = (
        student_data["student"].city
        or ""
    ).lower().strip()

    job_location = (
        job.location
        or ""
    ).lower().strip()

    if not job_location:

        location_score = 10

        reasons.append(
            "No specific location requirement"
        )

    elif student_city:

        if (
            student_city in job_location
            or job_location in student_city
        ):

            location_score = 10

            reasons.append(
                "Location matches"
            )

    score += location_score

    # ==================================================
    # 6. Work mode - 5 points
    # ==================================================

    work_mode_score = 0

    if (
        not job.work_mode
        or not preference
        or not preference.work_mode
    ):

        work_mode_score = 5

        reasons.append(
            "Work mode not restricted"
        )

    elif (
        job.work_mode.lower().strip()
        == preference.work_mode.lower().strip()
    ):

        work_mode_score = 5

        reasons.append(
            "Work mode matches"
        )

    score += work_mode_score

    # ==================================================
    # 7. Salary - 5 points
    # ==================================================

    salary_score = 0

    if (
        not preference
        or preference.min_salary is None
    ):

        salary_score = 5

        reasons.append(
            "Salary preference not restricted"
        )

    elif job.salary_max is not None:

        if (
            job.salary_max
            >= preference.min_salary
        ):

            salary_score = 5

            reasons.append(
                "Salary expectation matches"
            )

    elif job.salary_min is not None:

        if (
            job.salary_min
            >= preference.min_salary
        ):

            salary_score = 5

            reasons.append(
                "Salary expectation matches"
            )

    score += salary_score

    # ==================================================
    # 8. Employment type - 5 points
    # ==================================================

    employment_score = 0

    if (
        not job.employment_type
        or not preference
        or not preference.employment_type
    ):

        employment_score = 5

        reasons.append(
            "Employment type not restricted"
        )

    elif (
        job.employment_type.lower().strip()
        == preference.employment_type.lower().strip()
    ):

        employment_score = 5

        reasons.append(
            "Employment type matches"
        )

    score += employment_score

    # ==================================================
    # 9. Skills - 25 points
    # ==================================================

    skill_score = 0

    required_skills = (
        job.required_skills or []
    )

    if not required_skills:

        skill_score = 25

        reasons.append(
            "No specific skill requirement"
        )

    else:

        matched_skills = []

        for required_skill in required_skills:

            normalized_required = (
                normalize_skill_name(
                    required_skill
                )
            )

            if (
                normalized_required
                in student_skill_names
            ):

                matched_skills.append(
                    required_skill
                )

        skill_score = round(
            (
                len(matched_skills)
                /
                len(required_skills)
            )
            * 25
        )

        if matched_skills:

            reasons.append(
                "Skills matched: "
                + ", ".join(
                    matched_skills
                )
            )

        if (
            len(matched_skills)
            == len(required_skills)
        ):

            reasons.append(
                "All required skills matched"
            )

    score += skill_score

    score = min(
        score,
        100
    )

    return {
        "job_type": "internal",
        "job_id": job.id,
        "title": job.title,
        "company_id": job.company_id,
        "company_name": None,
        "location": job.location,
        "work_mode": job.work_mode,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "application_url": job.application_url,
        "source": job.source,
        "match_score": score,
        "reasons": reasons
    }

# ==================================================
# DETECT EXPERIENCE REQUIREMENT FROM EXTERNAL JOB
# ==================================================

def detect_external_experience_requirement(
    title: str,
    description: str
) -> dict:

    text = (
        f"{title or ''} "
        f"{description or ''}"
    )

    text = (
        text
        .lower()
        .replace("-", " ")
        .replace("_", " ")
    )

    # --------------------------------------------------
    # Fresher / entry-level
    # --------------------------------------------------

    if re.search(
        r"\b(fresher|freshers|entry level|entry-level|"
        r"graduate|graduates|0 years?|0 year experience)\b",
        text
    ):

        return {
            "type": "fresher",
            "min_months": 0
        }

    # --------------------------------------------------
    # Numeric experience
    # Examples:
    # 2 years
    # 2+ years
    # 3 to 5 years
    # 3-5 years
    # --------------------------------------------------

    range_match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*"
        r"(?:to|through)\s*"
        r"(\d+(?:\.\d+)?)\s*years?\b",
        text
    )

    if not range_match:

        range_match = re.search(
            r"\b(\d+(?:\.\d+)?)\s*"
            r"(?:-|–)\s*"
            r"(\d+(?:\.\d+)?)\s*years?\b",
            text
        )

    if range_match:

        min_years = float(
            range_match.group(1)
        )

        return {
            "type": "years",
            "min_months": round(
                min_years * 12
            )
        }

    plus_match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*\+\s*years?\b",
        text
    )

    if plus_match:

        min_years = float(
            plus_match.group(1)
        )

        return {
            "type": "years",
            "min_months": round(
                min_years * 12
            )
        }

    single_match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*years?\s*"
        r"(?:of\s*)?(?:relevant\s*)?experience\b",
        text
    )

    if single_match:

        min_years = float(
            single_match.group(1)
        )

        return {
            "type": "years",
            "min_months": round(
                min_years * 12
            )
        }

    # --------------------------------------------------
    # Senior / Lead
    #
    # We know experience is expected,
    # but we do NOT invent a number of years.
    # --------------------------------------------------

    if re.search(
        r"\b(senior|sr|lead|principal|manager)\b",
        title.lower()
    ):

        return {
            "type": "senior",
            "min_months": None
        }

    # --------------------------------------------------
    # No reliable experience requirement found
    # --------------------------------------------------

    return {
        "type": None,
        "min_months": None
    }

# ==================================================
# MATCH EXTERNAL JOB
# ==================================================

def calculate_external_job_match(
    job: ExternalJob,
    student_data: dict
) -> dict:

    preference = (
        student_data["preference"]
    )

    student_skill_names = (
        get_student_skill_names(
            student_data
        )
    )

    reasons = []

    # ==================================================
    # Available score
    #
    # Missing information is NOT treated as a mismatch.
    # We only score criteria that the job actually provides.
    # ==================================================

    score = 0
    maximum_score = 0

    # ==================================================
    # 1. Location - 20 points
    # ==================================================

    student_city = (
        student_data["student"].city
        or ""
    ).lower().strip()

    job_location = (
        job.location
        or ""
    ).lower().strip()

    if job_location:

        maximum_score += 20

        if (
            student_city
            and (
                student_city in job_location
                or job_location in student_city
            )
        ):

            score += 20

            reasons.append(
                "Location matches"
            )

        else:

            reasons.append(
                "Location does not match"
            )

    else:

        reasons.append(
            "Location not specified"
        )

    # ==================================================
    # 2. Work mode - 10 points
    # ==================================================

    if job.work_mode:

        maximum_score += 10

        if (
            preference
            and preference.work_mode
            and job.work_mode.lower().strip()
            ==
            preference.work_mode.lower().strip()
        ):

            score += 10

            reasons.append(
                "Work mode matches"
            )

        elif preference and preference.work_mode:

            reasons.append(
                "Work mode does not match"
            )

        else:

            reasons.append(
                "No work mode preference specified"
            )

    else:

        reasons.append(
            "Work mode not specified"
        )

    # ==================================================
    # 3. Salary - 10 points
    # ==================================================

    if (
        job.salary_min is not None
        or job.salary_max is not None
    ):

        maximum_score += 10

        salary_matches = False

        if (
            preference
            and preference.min_salary is not None
        ):

            if (
                job.salary_max is not None
                and job.salary_max
                >= preference.min_salary
            ):

                salary_matches = True

            elif (
                job.salary_min is not None
                and job.salary_min
                >= preference.min_salary
            ):

                salary_matches = True

        else:

            # Salary exists but student has no minimum.
            salary_matches = True

        if salary_matches:

            score += 10

            reasons.append(
                "Salary expectation matches"
            )

        else:

            reasons.append(
                "Salary does not meet expectation"
            )

    else:

        reasons.append(
            "Salary not specified"
        )

    # ==================================================
    # 4. Employment type - 10 points
    # ==================================================

    if job.employment_type:

        maximum_score += 10

        if (
            preference
            and preference.employment_type
            and job.employment_type.lower().strip()
            ==
            preference.employment_type.lower().strip()
        ):

            score += 10

            reasons.append(
                "Employment type matches"
            )

        elif preference and preference.employment_type:

            reasons.append(
                "Employment type does not match"
            )

        else:

            reasons.append(
                "No employment type preference specified"
            )

    else:

        reasons.append(
            "Employment type not specified"
        )
    # ==================================================
    # 5. Experience - 15 points
    # ==================================================

    experience_requirement = (
        detect_external_experience_requirement(
            job.title or "",
            job.description or ""
        )
    )

    student_experience_months = 0

    for experience in (
        student_data.get("experiences", [])
    ):

        if experience.duration_months:

            student_experience_months += (
                experience.duration_months
            )

    experience_type = (
        experience_requirement["type"]
    )

    required_months = (
        experience_requirement["min_months"]
    )

    if experience_type:

        maximum_score += 15

        # --------------------------------------------------
        # Fresher requirement
        # --------------------------------------------------

        if experience_type == "fresher":

            if student_experience_months == 0:

                score += 15

                reasons.append(
                    "Fresher requirement matches"
                )

            else:

                reasons.append(
                    "Fresher requirement does not match"
                )

        # --------------------------------------------------
        # Numeric experience requirement
        # --------------------------------------------------

        elif (
            experience_type == "years"
            and required_months is not None
        ):

            if (
                student_experience_months
                >= required_months
            ):

                score += 15

                reasons.append(
                    "Experience requirement satisfied"
                )

            elif student_experience_months > 0:

                partial_experience_score = round(
                    (
                        student_experience_months
                        /
                        required_months
                    )
                    * 15
                )

                partial_experience_score = min(
                    partial_experience_score,
                    15
                )

                score += (
                    partial_experience_score
                )

                reasons.append(
                    "Some relevant experience available"
                )

            else:

                reasons.append(
                    "Required experience not met"
                )

        # --------------------------------------------------
        # Senior / Lead requirement
        # --------------------------------------------------

        elif experience_type == "senior":

            if student_experience_months >= 36:

                score += 15

                reasons.append(
                    "Experience level matches senior/lead role"
                )

            elif student_experience_months > 0:

                score += 5

                reasons.append(
                    "Limited experience for senior/lead role"
                )

            else:

                reasons.append(
                    "Senior/lead role requires experience"
                )

    else:

        reasons.append(
            "Experience requirement not specified"
        )


    # ==================================================
    # 6. Skills - 40 points
    # ==================================================

    job_skills = (
        get_external_job_skills(
            job
        )
    )

    matched_skills = []

    for job_skill in job_skills:

        normalized_job_skill = (
            normalize_skill_name(
                job_skill
            )
        )

        if (
            normalized_job_skill
            in student_skill_names
        ):

            matched_skills.append(
                job_skill
            )

    if job_skills:

        maximum_score += 40

        skill_score = round(
            (
                len(matched_skills)
                /
                len(job_skills)
            )
            * 40
        )

        score += skill_score

        if matched_skills:

            reasons.append(
                "Skills matched: "
                + ", ".join(
                    matched_skills
                )
            )

        if (
            len(matched_skills)
            == len(job_skills)
        ):

            reasons.append(
                "All detected skills matched"
            )

    else:

        reasons.append(
            "No detected skill requirements"
        )

    # ==================================================
    # 7. Job title relevance - 10 points
    # ==================================================

    title_text = (
        job.title or ""
    )

    matched_title_skills = []

    for student_skill in student_skill_names:

        if text_contains_skill(
            title_text,
            student_skill
        ):

            matched_title_skills.append(
                student_skill
            )

    if title_text:

        maximum_score += 10

        if matched_title_skills:

            score += 10

            reasons.append(
                "Job title matches your skills"
            )

        else:

            reasons.append(
                "Job title does not directly match your skills"
            )

    # ==================================================
    # NORMALIZE SCORE
    #
    # Fixed denominator (not dependent on how much data
    # the job posting happens to include). A sparse
    # posting can no longer inflate to 100% just because
    # it's missing fields — missing fields simply earn
    # 0 points instead of being excluded from the total.
    # ==================================================

    TOTAL_POSSIBLE_SCORE = 115  # Location20 + WorkMode10 + Salary10 + Employment10 + Experience15 + Skills40 + Title10

    final_score = round(
        (
            score
            /
            TOTAL_POSSIBLE_SCORE
        )
        * 100
    )

    final_score = max(
        min(final_score, 100),
        0
    )

    # ==================================================
    # Return external job
    # ==================================================

    return {

        "job_type": "external",

        "job_id": job.id,

        "title": job.title,

        "company_id": None,

        "company_name": job.company_name,

        "location": job.location,

        "work_mode": job.work_mode,

        "salary_min": job.salary_min,

        "salary_max": job.salary_max,

        "employment_type": job.employment_type,

        "posted_date": job.posted_date,

        "description": job.description,

        "required_skills": job.required_skills,

        "application_url": job.application_url,

        "source": job.source,

        "match_score": final_score,

        "reasons": reasons
    }


# ==================================================
# GET MATCHING JOBS
# ==================================================

def get_matching_jobs(
    db: DBSession,
    user_id: int
) -> list[dict]:

    student_data = get_student_data(
        db,
        user_id
    )

    # ==================================================
    # Internal jobs
    # ==================================================

    internal_jobs = db.scalars(
        select(Job).where(
            Job.status == "ACTIVE"
        )
    ).all()

    # ==================================================
    # External jobs
    # ==================================================

    external_jobs = db.scalars(
        select(ExternalJob).where(
            ExternalJob.status == "active"
        )
    ).all()

    matches = []

    # ==================================================
    # Internal matching
    # ==================================================

    for job in internal_jobs:

        match = calculate_job_match(
            job,
            student_data
        )

        matches.append(
            match
        )

    # ==================================================
    # External matching
    # ==================================================

    for job in external_jobs:

        match = calculate_external_job_match(
            job,
            student_data
        )

        matches.append(
            match
        )

    # ==================================================
    # Highest score first
    # ==================================================

    matches.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    return matches