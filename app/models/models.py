from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class GovernmentMessage(Base):
    __tablename__ = "government_messages"

    id = Column(Integer, primary_key=True, index=True)
    organization = Column(String)
    department = Column(String)
    contactName = Column(String)
    email = Column(String)
    phone = Column(String)
    country = Column(String)
    message = Column(String)
    priority = Column(String)
    createdAt = Column(DateTime, server_default=func.now())

