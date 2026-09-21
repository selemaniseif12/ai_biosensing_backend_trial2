from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt

from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    # FIX: use user.password instead of user.password_hash
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_user(db: Session, user_data: UserCreate):
    hashed_pw = get_password_hash(user_data.password)
    # FIX: store hashed password in `password`, not `password_hash`
    db_user = User(
        email=user_data.email,
        password=hashed_pw,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def register_user(db: Session, user_data: UserCreate):
    return create_user(db, user_data)


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
