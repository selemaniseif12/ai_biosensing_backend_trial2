from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import Base
from app.utils.token_generator import generate_token


class ServiceToken(Base):
    __tablename__ = "service_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    service_name = Column(String, nullable=False)
    user_id = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def create_token(db: Session, service_name: str, user_id: int | None = None):
        token_value = generate_token()

        record = ServiceToken(
            token=token_value,
            service_name=service_name,
            user_id=user_id,
            is_active=True,
            created_at=datetime.utcnow()
        )

        db.add(record)
        db.commit()
        db.refresh(record)
        return record
