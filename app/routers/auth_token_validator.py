from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.token_model import ServiceToken


def validate_service_token(token: str, service_name: str, db: Session = Depends(get_db)):
    """
    Unified token validator for all ML endpoints.
    Ensures:
    - token exists
    - token is active
    - token matches service_name
    - token is not expired
    """

    token_obj = (
        db.query(ServiceToken)
        .filter(ServiceToken.token == token)
        .first()
    )

    if not token_obj:
        raise HTTPException(status_code=401, detail="Invalid token")

    if not token_obj.is_active:
        raise HTTPException(status_code=403, detail="Token disabled by admin")

    if token_obj.token_type != service_name:
        raise HTTPException(status_code=403, detail="Token not authorized for this service")

    if token_obj.expires_at and token_obj.expires_at < datetime.utcnow():
        raise HTTPException(status_code=403, detail="Token expired")

    return token_obj
