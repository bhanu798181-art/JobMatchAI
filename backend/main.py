from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --------------------------------------------------
# Authentication
# --------------------------------------------------

from auth.routes import router as auth_router


# --------------------------------------------------
# Models
# --------------------------------------------------

from models.student_profile import StudentProfile
from models.job_preference import JobPreference
from models.resume import Resume
from models.job_application import JobApplication
from models.job import Job
from models.company_profile import CompanyProfile
from external_jobs.models import ExternalJob


# --------------------------------------------------
# Routes
# --------------------------------------------------

from profile.routes import router as profile_router
from preferences.routes import router as preferences_router
from resume.routes import router as resume_router
from applications.routes import router as applications_router
from jobs.routes import router as jobs_router
from matching.routes import router as matching_router
from external_jobs.routes import router as external_jobs_router


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="JobMatch AI"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://job-match-ai-two.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Authentication routes
# --------------------------------------------------

app.include_router(
    auth_router
)


# --------------------------------------------------
# Student profile routes
# --------------------------------------------------

app.include_router(
    profile_router
)


# --------------------------------------------------
# Job preference routes
# --------------------------------------------------

app.include_router(
    preferences_router
)


# --------------------------------------------------
# Resume routes
# --------------------------------------------------

app.include_router(
    resume_router
)


# --------------------------------------------------
# Job application routes
# --------------------------------------------------

app.include_router(
    applications_router
)


# --------------------------------------------------
# Job routes
# --------------------------------------------------

app.include_router(
    jobs_router
)


# --------------------------------------------------
# Job matching routes
# --------------------------------------------------

app.include_router(
    matching_router
)


# --------------------------------------------------
# External job routes
# --------------------------------------------------

app.include_router(
    external_jobs_router
)


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "JobMatch AI API is running"
    }