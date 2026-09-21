from app.models.user import User
from app.schemas.auth import UserCreate
from app.core.security import hash_password, verify_password
from sqlalchemy.orm import Session

def register_user(db: Session, user_data: UserCreate):
    # Hash the password
    hashed_pw = hash_password(user_data.password)

    # Create user instance
    new_user = User(
        email=user_data.email,
        password=hashed_pw,
        full_name=user_data.full_name,
    )

    # Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def authenticate_user(db: Session, email: str, password: str):
    # Find user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    # Verify password
    if not verify_password(password, user.password):
        return None

    return user
