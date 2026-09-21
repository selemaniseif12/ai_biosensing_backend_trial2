from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class CourseContent(Base):
    __tablename__ = "course_content"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), index=True)
    module_number = Column(Integer, index=True)
    video = Column(String)
    slides_pdf = Column(String)
    website = Column(String)
    quiz_file = Column(String)

  
