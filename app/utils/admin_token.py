from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.token_model import TokenModel


def validate_admin_token(token: str) -> bool:
    if not token or not isinstance(token, str):
        return False

    db: Session = SessionLocal()
    try:
        record = (
            db.query(TokenModel)
            .filter(
                TokenModel.token == token,
                TokenModel.token_type == "admin_system",
                TokenModel.is_active.is_(True),
            )
            .first()
        )

        if record is None:
            return False

        if record.expires_at is not None:
            from datetime import datetime

            expiry = record.expires_at
            now = datetime.now(expiry.tzinfo) if expiry.tzinfo else datetime.utcnow()

            if expiry <= now:
                return False

        return True
    finally:
        db.close()
