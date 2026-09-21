from sqlalchemy import Column, Integer, String, Float
from app.database import Base, engine, SessionLocal

class Virus(Base):
    __tablename__ = "viruses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    mass_fg = Column(Float, nullable=False)

    family = Column(String, nullable=True)
    description = Column(String, nullable=True)