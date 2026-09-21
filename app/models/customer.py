from sqlalchemy import Column, Integer, String
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    organization = Column(String(255))
    phone = Column(String(50))

    # Removed APIKey relationship because APIKey model does not exist
    # This fixes the SQLAlchemy InvalidRequestError during startup
