# app/services/outline_seed.py

from sqlalchemy.orm import Session
from app.crud.course import create_course, create_module, create_lesson
from app.schemas.course import CourseCreate, ModuleCreate, LessonCreate


def seed_course_outline(db: Session):
    # ---------------------------------------------------------
    # Seed ONE course
    # ---------------------------------------------------------
    course = create_course(db, CourseCreate(
        title="Full-Stack API Engineering",
        description="Learn backend engineering with a structured, module-based course.",
        price=49,
        duration="6 weeks",
        category="software",
        status="published"
    ))

    # ---------------------------------------------------------
    # Module 1
    # ---------------------------------------------------------
    module1 = create_module(db, ModuleCreate(
        title="Foundations of API Engineering",
        description="Core concepts of APIs.",
        order=1
    ), course_id=course.id)

    create_lesson(db, LessonCreate(
        title="Lesson 1: What is an API?",
        description="Understanding the basics of API design.",
        video_url="lesson1.mp4",
        slides_urls=[]
    ), module_id=module1.id)

    # ---------------------------------------------------------
    # Module 2
    # ---------------------------------------------------------
    module2 = create_module(db, ModuleCreate(
        title="Advanced API Engineering",
        description="Authentication, rate limiting, and security.",
        order=2
    ), course_id=course.id)

    create_lesson(db, LessonCreate(
        title="Lesson 2: API Authentication",
        description="Learn how authentication works in modern APIs.",
        video_url="lesson2.mp4",
        slides_urls=[]
    ), module_id=module2.id)

    return {"message": "Course outline seeded successfully"}
