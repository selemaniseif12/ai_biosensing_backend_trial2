from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    # Meeting details
    topic = Column(String, nullable=False)
    details = Column(Text)
    priority = Column(String, default="normal")
    scheduled_time = Column(DateTime, nullable=True)
    status = Column(String, default="scheduled")

    # Relationship to Team
    team = relationship("Team")
