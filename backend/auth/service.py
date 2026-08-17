from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.password import hash_password
from auth.schemas import RegisterRequest
from models.user import User


def register_user(db: Session, data: RegisterRequest) -> User:
    # 1. Check whether the email already exists
    existing_user = db.scalar(
        select(User).where(User.email == data.email)
    )

    if existing_user:
        raise ValueError("Email is already registered")

    # 2. Hash the password
    password_hash = hash_password(data.password)

    # 3. Create the new user
    user = User(
        email=data.email,
        password_hash=password_hash,
        role=data.role,
        is_active=True
    )

    # 4. Add the user to the database
    db.add(user)

    # 5. Save the change
    db.commit()

    # 6. Refresh so generated values such as ID are available
    db.refresh(user)

    return user