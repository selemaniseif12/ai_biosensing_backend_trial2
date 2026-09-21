from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CourseModule(Base):
    __tablename__ = "course_modules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    module_number = Column(Integer)

    title = Column(String)
    description = Column(String)
    video_description = Column(String)
    slide_description = Column(String)
    pdf_description = Column(String)
    website_description = Column(String)

    # Store lessons as a JSON string
    lessons = Column(String)

    quiz = Column(String)
    quiz_file = Column(String)
    assignment = Column(String)
    assignment_file = Column(String)

    course = relationship("Course", back_populates="modules")
