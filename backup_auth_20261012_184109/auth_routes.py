from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.auth import UserLogin
from app.auth.auth import authenticate_user, create_access_token
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Authenticate user
    user = authenticate_user(db, user_data.email, user_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # ⭐ CRITICAL FIX: include "sub" so get_current_user works
    access_token = create_access_token({"sub": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }
