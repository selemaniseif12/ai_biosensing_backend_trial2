# app/db_models/api_key_model.py

import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from app.database import Base
  # <-- FIXED


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)

    key = Column(String(128), unique=True, index=True, nullable=False)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    name = Column(String(100), nullable=True)

    active = Column(Boolean, default=True, nullable=False)
    revoked_at = Column(DateTime, nullable=True)

    total_calls = Column(Integer, default=0, nullable=False)

    monthly_limit = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    customer = relationship("Customer", back_populates="api_keys")

    @staticmethod
    def generate_key() -> str:
        return uuid.uuid4().hex + uuid.uuid4().hex
