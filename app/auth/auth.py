from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

# Use the SAME scheme everywhere
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Shared secret key
SECRET_KEY = "564cc7b73913e7206a15fd72385738d779e04957686233143ffe68b22c77b5c7"
ALGORITHM = "HS256"


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        # Decode JWT using the correct shared secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Fetch user from database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
