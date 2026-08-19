from fastapi import FastAPI

from auth.routes import router as auth_router
from models.student_profile import StudentProfile
from profile.routes import router as profile_router


app = FastAPI(title="JobMatch AI")


app.include_router(auth_router)
app.include_router(profile_router)


@app.get("/")
def home():
    return {"message": "JobMatch AI API is running"}