# models/service_model.py

from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(String, unique=True, index=True, nullable=False)   # e.g. "ml_v2"
    name = Column(String, nullable=False)                                  # Human-readable name
    type = Column(String, nullable=False)                                  # service | course | digital | physical
    active = Column(Boolean, default=True)                                 # Can be purchased
    coming_soon = Column(Boolean, default=False)                           # Not yet available
