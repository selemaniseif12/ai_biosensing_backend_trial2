from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.token_model import TokenModel


def validate_token(db: Session, token: str, service_name: str):
    """
    Validate a token for a specific service.

    Returns the token record if valid.
    Raises HTTPException if invalid or expired.
    """

    token_record = db.query(TokenModel).filter(
        TokenModel.token == token,
        TokenModel.token_type == service_name,
        TokenModel.is_active == True
    ).first()

    if not token_record:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return token_record
