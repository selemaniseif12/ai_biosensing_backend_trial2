from sqlalchemy.orm import Session
from app.schemas.course import CourseCreate
from app.crud.course import create_course, get_course, list_courses

class CourseService:

    @staticmethod
    def create(db: Session, payload: CourseCreate):
        return create_course(db, payload)

    @staticmethod
    def get(db: Session, course_id: int):
        return get_course(db, course_id)

    @staticmethod
    def list(db: Session):
        return list_courses(db)
