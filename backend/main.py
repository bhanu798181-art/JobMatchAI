from fastapi import FastAPI

from auth.routes import router as auth_router
from models.student_profile import StudentProfile
from models.job_preference import JobPreference
from models.resume import Resume
from models.job_application import JobApplication
from profile.routes import router as profile_router
from preferences.routes import router as preferences_router
from resume.routes import router as resume_router
from applications.routes import router as applications_router


app = FastAPI(title="JobMatch AI")


app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(preferences_router)
app.include_router(resume_router)
app.include_router(applications_router)


@app.get("/")
def home():
    return {
        "message": "JobMatch AI API is running"
    }