from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import create_access_token
from app.database import get_db
from app.schemas.auth import UserCreate, UserLogin
from app.services.auth_service import authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["Auth"])
ADMIN_EMAIL = "selemaniseif1974@gmail.com"


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = register_user(db, user)
    # Never return the stored password hash from a registration endpoint.
    return {
        "id": new_user.id,
        "email": new_user.email,
        "full_name": new_user.full_name,
        "role": new_user.role,
    }


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Preserve the existing admin assignment, but compare normalized email.
    # Public registration explicitly blocks this reserved administrator address.
    role = "admin" if db_user.email.strip().lower() == ADMIN_EMAIL else "student"
    token = create_access_token({"sub": db_user.id, "role": role})

    return {
        "access_token": token,
        "token_type": "bearer",
        "email": db_user.email,
        "user_id": db_user.id,
        "role": role,
    }
