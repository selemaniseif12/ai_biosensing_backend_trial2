from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import UserCreate, UserLogin
from app.services.auth_service import register_user, authenticate_user
from app.auth import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# -----------------------------
# REGISTER NEW USER
# -----------------------------
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)


# -----------------------------
# LOGIN USER
# -----------------------------
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Assign admin role based on your email
    role = "admin" if db_user.email == "selemaniseif1974@gmail.com" else "student"

    # Create JWT token containing user_id + role
    token = create_access_token({
        "sub": db_user.id,
        "role": role
    })

    return {
        "access_token": token,
        "email": db_user.email,
        "user_id": db_user.id,
        "role": role
    }
