from sqlalchemy import text
from sqlalchemy.orm import Session

from database import engine


db = Session(engine)

db.execute(
    text("""
        INSERT INTO company_profiles (
            user_id,
            company_name,
            website,
            industry,
            description,
            is_verified
        )
        VALUES (
            :user_id,
            :company_name,
            :website,
            :industry,
            :description,
            :is_verified
        )
    """),
    {
        "user_id": 8,
        "company_name": "Tech Solutions",
        "website": "https://techsolutions.example.com",
        "industry": "Software Development",
        "description": "Technology company hiring software developers.",
        "is_verified": True
    }
)

db.commit()

print("Company profile created successfully")
