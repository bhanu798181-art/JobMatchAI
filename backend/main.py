from fastapi import FastAPI

from auth.routes import router as auth_router


app = FastAPI(title="JobMatch AI")


app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "JobMatch AI API is running"}