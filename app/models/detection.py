from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base, engine, SessionLocal


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    virus_id = Column(Integer, ForeignKey("viruses.id"))
    device_id = Column(Integer, ForeignKey("devices.id"))

    physics_estimated_count = Column(Float)
    physics_mass_change_fg = Column(Float)

    ml_estimated_time_to_detection = Column(Float, nullable=True)
    ml_confidence = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
