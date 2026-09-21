# app/models/activity.py

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base  # adjust import if needed


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, index=True, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    module_id = Column(Integer, ForeignKey("course_modules.id"), nullable=True)
    content_id = Column(Integer, ForeignKey("course_content.id"), nullable=True)

    action = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Optional relationships (not required but useful)
    course = relationship("Course", backref="activities")
    module = relationship("CourseModule", backref="activities")
    content = relationship("CourseContent", backref="activities")
