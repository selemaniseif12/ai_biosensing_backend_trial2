# app/models/consulting_model.py

from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class ConsultingRequestModel(Base):
    __tablename__ = "consulting_requests"

    id = Column(Integer, primary_key=True, index=True)

    # Basic fields
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    # Optional fields
    organization = Column(String(255), nullable=True)
    api_key = Column(String(255), nullable=True)

    # Long text fields
    project_description = Column(Text, nullable=False)

    # Services list stored as comma-separated text
    services = Column(Text, nullable=False)
