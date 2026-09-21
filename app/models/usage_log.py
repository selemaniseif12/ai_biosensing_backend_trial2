from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.database import Base # <-- FIXED

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True)
    event = Column(String(255))
    detail = Column(String(500))
    created_at = Column(TIMESTAMP)
