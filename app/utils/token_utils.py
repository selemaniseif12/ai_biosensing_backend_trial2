from datetime import datetime
from sqlalchemy.orm import Session
from app.models.token_model import TokenModel


def is_token_active(db: Session, token: str, required_type: str):
    """
    Strict single-type token validation.
    Checks:
    - token exists
    - token_type matches required_type
    - token is active
    - token is not expired
    """
    db_token = db.query(TokenModel).filter(TokenModel.token == token).first()

    if not db_token:
        return False

    if db_token.token_type != required_type:
        return False

    if not db_token.is_active:
        return False

    if db_token.expires_at is not None and db_token.expires_at < datetime.utcnow():
        return False

    return True


def is_any_valid_token(db: Session, token: str, allowed_types: list[str]):
    """
    Multi-type token validation.
    Example:
        allowed_types = ["ml_v6"]
    """
    db_token = db.query(TokenModel).filter(TokenModel.token == token).first()

    if not db_token:
        return False

    if db_token.token_type not in allowed_types:
        return False

    if not db_token.is_active:
        return False

    if db_token.expires_at is not None and db_token.expires_at < datetime.utcnow():
        return False

    return True
