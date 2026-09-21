from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.enrollment import Enrollment
from app.models.course import Course


router = APIRouter(prefix="/enrollment", tags=["Enrollment"])

# 1. Enroll student in a course
@router.post("/{course_id}")
def enroll(course_id: int, user_id: int, db: Session = Depends(get_db)):
    # Check course exists
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check if already enrolled
    existing = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == course_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled")

    enrollment = Enrollment(
        user_id=user_id,
        course_id=course_id,
        payment_status="paid",      # Stripe will set this
        enrollment_status="active"
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return {"message": "Enrollment successful", "enrollment": enrollment}


# 2. Check enrollment status
@router.get("/status/{course_id}")
def enrollment_status(course_id: int, user_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == course_id
    ).first()

    return {
        "enrolled": enrollment is not None,
        "course_id": course_id,
        "status": enrollment.enrollment_status if enrollment else "not_enrolled"
    }


# 3. Get all courses a student is enrolled in
@router.get("/my-courses")
def my_courses(user_id: int, db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).filter(
        Enrollment.user_id == user_id
    ).all()

    return {"courses": [e.course_id for e in enrollments]}


# 4. Admin: list all enrollments
@router.get("/all")
def all_enrollments(db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).all()
    return enrollments
