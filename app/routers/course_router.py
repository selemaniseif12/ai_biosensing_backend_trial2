from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.course import Course
from app.models.course_module import CourseModule
from app.models.course_content import CourseContent
from pydantic import BaseModel

router = APIRouter()

# ---------------------------
# Pydantic Schemas
# ---------------------------

class CourseCreate(BaseModel):
    title: str
    description: str | None = None
    price: int | None = None
    duration: str | None = None
    category: str | None = None
    status: str | None = None

class CourseResponse(BaseModel):
    id: int
    title: str
    description: str | None
    price: int | None
    duration: str | None
    category: str | None
    status: str | None

    class Config:
        orm_mode = True

# ---------------------------
# Endpoints
# ---------------------------

@router.get("/course/", response_model=list[CourseResponse])
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@router.post("/course/", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.get("/course/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.delete("/course/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.query(CourseModule).filter(CourseModule.course_id == course_id).delete()
    db.query(CourseContent).filter(CourseContent.course_id == course_id).delete()

    db.delete(course)
    db.commit()
    return
