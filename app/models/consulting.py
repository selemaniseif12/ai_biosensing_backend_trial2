from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from app.database import Base

# IMPORTANT:
# We reference Team using a string, NOT by importing the class.
# This avoids circular imports and fixes your error.

class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    user_id = Column(Integer, nullable=False)

    # Meeting details
    topic = Column(String, nullable=False)
    details = Column(Text)
    priority = Column(String, default="normal")
    scheduled_time = Column(DateTime, nullable=True)
    status = Column(String, default="scheduled")

    # FIXED: Use string-based relationship to avoid load-order errors
    team = relationship("Team", backref="consultations")
