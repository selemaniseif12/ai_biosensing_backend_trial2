from fastapi import Depends, Header, HTTPException, status
from app.auth.auth import get_current_user

# ⭐ This replaces Firebase authentication entirely.
# ⭐ It simply reuses your existing JWT system.

async def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )

    token = authorization.split(" ")[1]

    # ⭐ Use your existing JWT validator
    try:
        user = get_current_user(token=token)
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
