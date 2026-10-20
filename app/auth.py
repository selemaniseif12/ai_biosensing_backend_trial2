import os
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User


# ---------------------------------------------------------
# AUTHENTICATION CONFIGURATION
# ---------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Read the JWT signing secret from the backend environment.
# This is separate from STRIPE_SECRET_KEY.
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET_KEY is not configured. "
        "Set it in the backend .env file or deployment environment."
    )


# ---------------------------------------------------------
# CREATE JWT TOKEN WITH ROLE
# ---------------------------------------------------------

def create_access_token(data: dict):
    """
    Create a JWT access token.

    JWT requires the 'sub' (subject) claim to be a string.
    Convert a numeric database user ID to a string before signing.
    """

    to_encode = data.copy()

    if to_encode.get("sub") is not None:
        to_encode["sub"] = str(to_encode["sub"])

    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ---------------------------------------------------------
# VALIDATE TOKEN AND RETURN AUTHENTICATED USER
# ---------------------------------------------------------

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Validate the JWT and return the corresponding database user.

    The user ID is obtained from the verified token, rather than
    a user_id parameter supplied by the browser.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        raw_user_id = payload.get("sub")
        role = payload.get("role")

        if raw_user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Database IDs are integers, although JWT subjects are strings.
        try:
            user_id = int(raw_user_id)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=401,
                detail="Invalid user ID in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user_id < 1:
            raise HTTPException(
                status_code=401,
                detail="Invalid user ID in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Look up the user identified by the verified JWT.
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Preserve the role carried by the JWT.
    user.role = role

    return user