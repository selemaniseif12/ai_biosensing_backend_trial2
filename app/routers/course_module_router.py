from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.course_module import CourseModule
from pydantic import BaseModel
from typing import List, Optional
import json

router = APIRouter()

# ---------------------------
# Pydantic Schemas
# ---------------------------

class ModuleCreate(BaseModel):
    course_id: int
    module_number: int
    title: str
    description: str

    video_description: Optional[str] = None
    slide_description: Optional[str] = None
    pdf_description: Optional[str] = None
    website_description: Optional[str] = None

    lessons: Optional[List[str]] = None
    quiz: Optional[str] = None
    quiz_file: Optional[str] = None
    assignment: Optional[str] = None
    assignment_file: Optional[str] = None


class ModuleResponse(ModuleCreate):
    id: int

    class Config:
        orm_mode = True

# ---------------------------
# Endpoints
# ---------------------------

@router.post("/course-modules/", response_model=ModuleResponse)
def create_module(module: ModuleCreate, db: Session = Depends(get_db)):
    new_module = CourseModule(
        course_id=module.course_id,
        module_number=module.module_number,
        title=module.title,
        description=module.description,

        video_description=module.video_description,
        slide_description=module.slide_description,
        pdf_description=module.pdf_description,
        website_description=module.website_description,

        lessons=json.dumps(module.lessons) if module.lessons else None,
        quiz=module.quiz,
        quiz_file=module.quiz_file,
        assignment=module.assignment,
        assignment_file=module.assignment_file
    )

    db.add(new_module)
    db.commit()
    db.refresh(new_module)

    # ⭐ Convert JSON string → list before returning
    if new_module.lessons:
        new_module.lessons = json.loads(new_module.lessons)

    return new_module


@router.get("/course-modules/course/{course_id}", response_model=list[ModuleResponse])
def get_modules(course_id: int, db: Session = Depends(get_db)):
    modules = db.query(CourseModule).filter(CourseModule.course_id == course_id).all()

    # ⭐ Convert JSON string → list for each module
    for m in modules:
        if m.lessons:
            m.lessons = json.loads(m.lessons)

    return modules


@router.put("/course-modules/{module_id}", response_model=ModuleResponse)
def update_module(module_id: int, module: ModuleCreate, db: Session = Depends(get_db)):
    existing = db.query(CourseModule).filter(CourseModule.id == module_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Module not found")

    existing.course_id = module.course_id
    existing.module_number = module.module_number
    existing.title = module.title
    existing.description = module.description

    existing.video_description = module.video_description
    existing.slide_description = module.slide_description
    existing.pdf_description = module.pdf_description
    existing.website_description = module.website_description

    existing.lessons = json.dumps(module.lessons) if module.lessons else None
    existing.quiz = module.quiz
    existing.quiz_file = module.quiz_file
    existing.assignment = module.assignment
    existing.assignment_file = module.assignment_file

    db.commit()
    db.refresh(existing)

    # ⭐ Convert JSON string → list before returning
    if existing.lessons:
        existing.lessons = json.loads(existing.lessons)

    return existing


@router.delete("/course-modules/{module_id}", status_code=204)
def delete_module(module_id: int, db: Session = Depends(get_db)):
    module = db.query(CourseModule).filter(CourseModule.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    db.delete(module)
    db.commit()
    return
