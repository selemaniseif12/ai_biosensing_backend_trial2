# app/models_v6_logs.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.models.database import engine


class AnalyzerV6Log(Base):
    __tablename__ = "analyzer_v6_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    version = Column(String, default="v6")
    device_id = Column(String, index=True)
    virus = Column(String)

    deposition_rate = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    flow_rate = Column(Float)
    mass_of_virus = Column(Float)

    predicted_time_to_detection = Column(Float)
