from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.database import Base # <-- FIXED

class MLLog(Base):
    __tablename__ = "ml_logs"

    id = Column(Integer, primary_key=True)
    action = Column(String(255))
    detail = Column(String(500))
    created_at = Column(TIMESTAMP)
