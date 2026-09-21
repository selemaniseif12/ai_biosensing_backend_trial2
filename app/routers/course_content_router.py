from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.course_content import CourseContent
from app.schemas.course_content import CourseContentCreate, CourseContentResponse

router = APIRouter(
    prefix="/course-content",
    tags=["Course Content"]
)

@router.post("/", response_model=CourseContentResponse)
def create_course_content(payload: CourseContentCreate, db: Session = Depends(get_db)):
    content = CourseContent(**payload.dict())
    db.add(content)
    db.commit()
    db.refresh(content)
    return content

@router.get("/{course_id}", response_model=List[CourseContentResponse])
def get_course_content(course_id: int, db: Session = Depends(get_db)):
    content = db.query(CourseContent).filter(
        CourseContent.course_id == course_id
    ).all()

    if not content:
        raise HTTPException(status_code=404, detail="Course not found")

    return content

# ⭐ NEW DELETE ENDPOINT
@router.delete("/{id}", status_code=204)
def delete_course_content(id: int, db: Session = Depends(get_db)):
    content = db.query(CourseContent).filter(
        CourseContent.id == id
    ).first()

    if not content:
        raise HTTPException(status_code=404, detail="Course content not found")

    db.delete(content)
    db.commit()
    return
