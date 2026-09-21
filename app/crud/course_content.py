from sqlalchemy.orm import Session
from app.models.course_content import CourseContent
from app.schemas.course_content import CourseContentCreate
import json

def save_course_content(db: Session, payload: CourseContentCreate):
    db_content = CourseContent(
        course_id=payload.course_id,
        content_json=json.dumps(payload.dict())
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content


def get_course_content_by_course(db: Session, course_id: int):
    return db.query(CourseContent).filter(CourseContent.course_id == course_id).first()


def update_course_content(db: Session, course_id: int, payload: CourseContentCreate):
    db_content = db.query(CourseContent).filter(CourseContent.course_id == course_id).first()
    if not db_content:
        return None

    db_content.content_json = json.dumps(payload.dict())

    db.commit()
    db.refresh(db_content)
    return db_content
