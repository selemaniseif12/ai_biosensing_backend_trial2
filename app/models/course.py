from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Integer)
    duration = Column(String)
    category = Column(String)
    status = Column(String)

    modules = relationship("CourseModule", back_populates="course")
