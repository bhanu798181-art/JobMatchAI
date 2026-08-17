import secrets
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from auth.password import hash_password, verify_password
from auth.schemas import LoginRequest, RegisterRequest
from models.session import Session
from models.user import User


def register_user(db: DBSession, data: RegisterRequest) -> User:
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


def login_user(db: DBSession, data: LoginRequest) -> tuple[User, str]:
    # 1. Look up the user by email
    user = db.scalar(
        select(User).where(User.email == data.email)
    )

    # 2. Generic error if user doesn't exist
    if not user:
        raise ValueError("Invalid email or password")

    # 3. Check that the account is active
    if not user.is_active:
        raise ValueError("Invalid email or password")

    # 4. Verify the password against the stored hash
    if not verify_password(data.password, user.password_hash):
        raise ValueError("Invalid email or password")

    # 5. Generate a secure random session token
    session_token = secrets.token_urlsafe(32)

    # 6. Create a session that expires after 7 days
    session = Session(
        session_token=session_token,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )

    # 7. Add the session to the database
    db.add(session)

    # 8. Save the session
    db.commit()

    return user, session_token


def get_user_from_session(
    db: DBSession,
    session_token: str
) -> User:
    # 1. Find the session by its token
    session = db.scalar(
        select(Session).where(
            Session.session_token == session_token
        )
    )

    # 2. Session doesn't exist
    if not session:
        raise ValueError("Invalid or expired session")

    # 3. Session has been deactivated
    if not session.is_active:
        raise ValueError("Invalid or expired session")

    # 4. Session has expired
    if session.expires_at <= datetime.utcnow():
        session.is_active = False
        db.commit()

        raise ValueError("Invalid or expired session")

    # 5. Find the user associated with this session
    user = db.scalar(
        select(User).where(
            User.id == session.user_id
        )
    )

    # 6. User doesn't exist or account is disabled
    if not user or not user.is_active:
        raise ValueError("Invalid or expired session")

    return user


def logout_user(
    db: DBSession,
    session_token: str
) -> None:
    # 1. Find the session
    session = db.scalar(
        select(Session).where(
            Session.session_token == session_token
        )
    )

    # 2. If the session doesn't exist, there is nothing to do
    if not session:
        return

    # 3. Deactivate the session
    session.is_active = False

    # 4. Save the change
    db.commit()