from sqlalchemy.orm import Session
from app.schemas.course_content import CourseContentCreate
from app.crud.course_content import (
    save_course_content,
    get_course_content_by_course,
    update_course_content
)

class ContentService:

    @staticmethod
    def save(db: Session, payload: CourseContentCreate):
        return save_course_content(db, payload)

    @staticmethod
    def get(db: Session, course_id: int):
        return get_course_content_by_course(db, course_id)

    @staticmethod
    def update(db: Session, course_id: int, payload: CourseContentCreate):
        return update_course_content(db, course_id, payload)
