from sqlalchemy import Column, Integer, String
from app.database import Base

class ConsultationSchedule(Base):
    __tablename__ = "consultation_schedule"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    participants = Column(String, nullable=False)
