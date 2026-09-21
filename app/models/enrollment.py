from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    payment_status = Column(String, default="pending")  # pending, paid
    enrollment_status = Column(String, default="active")  # active, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
