from sqlalchemy import Column, Integer, String
from app.database import Base

class Device(Base):
    __tablename__ = "devices"   # MUST match ForeignKey("devices.id")

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Optional fields
    location = Column(String, nullable=True)
    status = Column(String, nullable=True)
