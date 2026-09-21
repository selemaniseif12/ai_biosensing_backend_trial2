from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    plan_name = Column(String, nullable=False)
    status = Column(String, default="active")
    payment_reference = Column(String, nullable=True)

    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)

    # ⭐ THIS IS WHAT WAS MISSING
   
