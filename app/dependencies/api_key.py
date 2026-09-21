from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.crud.api_keys import (
    get_api_key_by_value,
    increment_usage
)

def require_api_key(
    x_api_key: str = Header(None, alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    """
    Validates the API key sent in the X-API-Key header.
    Enforces:
    - Key exists
    - Key is active
    - Monthly usage limits (if set)
    - Usage counter increments
    """

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header"
        )

    api_key = get_api_key_by_value(db, x_api_key)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )

    if not api_key.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key is inactive or revoked"
        )

    if api_key.monthly_limit > 0 and api_key.total_calls >= api_key.monthly_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="API key monthly usage limit exceeded"
        )

    increment_usage(db, api_key)

    return api_key
