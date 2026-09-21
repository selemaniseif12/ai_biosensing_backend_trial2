from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base

class TokenModel(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    token_type = Column(String, nullable=False)
    user_id = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    @staticmethod
    def create_token(db, token_type: str, user_id=None, description=None):
        import secrets
        token_value = secrets.token_hex(16)

        token = TokenModel(
            token=token_value,
            token_type=token_type,
            user_id=user_id,
            description=description,
            is_active=True,
            created_at=datetime.utcnow()
        )

        db.add(token)
        db.commit()
        db.refresh(token)
        return token
