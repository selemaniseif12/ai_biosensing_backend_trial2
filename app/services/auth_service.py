from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.auth import UserCreate


ADMIN_EMAIL = "selemaniseif1974@gmail.com"


def normalize_email(email: str) -> str:
    return str(email).strip().lower()


def register_user(db: Session, user_data: UserCreate):
    email = normalize_email(str(user_data.email))

    # Do not permit public self-registration of the administrator address.
    # The existing administrator must use the already-established account.
    if email == ADMIN_EMAIL:
        raise HTTPException(
            status_code=403,
            detail="This administrator email cannot be registered through public sign-up.",
        )

    existing_user = (
        db.query(User)
        .filter(func.lower(User.email) == email)
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists. Please sign in instead.",
        )

    new_user = User(
        email=email,
        password=hash_password(user_data.password),
        full_name=user_data.full_name.strip(),
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists. Please sign in instead.",
        ) from exc
    except Exception:
        db.rollback()
        raise

    return new_user


def authenticate_user(db: Session, email: str, password: str):
    normalized_email = normalize_email(email)
    user = (
        db.query(User)
        .filter(func.lower(User.email) == normalized_email)
        .first()
    )
    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user