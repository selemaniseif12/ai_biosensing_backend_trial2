# app/services/enrollment_service.py

from sqlalchemy.orm import Session
from app.models.enrollment import Enrollment
from app.models.course import Course


def activate_enrollment(db: Session, user_id: int, course_id: int):
    """
    Called from Stripe webhook after successful payment.
    Creates an active enrollment if not already enrolled.
    """

    existing = (
        db.query(Enrollment)
        .filter(Enrollment.user_id == user_id,
                Enrollment.course_id == course_id)
        .first()
    )

    if existing:
        # Already enrolled, just return it
        return existing

    enrollment = Enrollment(
        user_id=user_id,
        course_id=course_id,
        status="active"
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment


def check_enrollment(db: Session, user_id: int, course_id: int):
    """
    Returns True/False depending on whether the user is enrolled.
    """

    enrollment = (
        db.query(Enrollment)
        .filter(Enrollment.user_id == user_id,
                Enrollment.course_id == course_id,
                Enrollment.status == "active")
        .first()
    )

    return enrollment is not None


def get_my_courses(db: Session, user_id: int):
    """
    Returns a list of courses the user is enrolled in.
    """

    enrollments = (
        db.query(Enrollment)
        .filter(Enrollment.user_id == user_id,
                Enrollment.status == "active")
        .all()
    )

    course_ids = [e.course_id for e in enrollments]

    courses = (
        db.query(Course)
        .filter(Course.id.in_(course_ids))
        .all()
    )

    return courses
