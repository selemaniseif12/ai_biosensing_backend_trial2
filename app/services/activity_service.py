# app/services/activity_service.py

from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate


def log_activity(db: Session, data: ActivityCreate):
    """
    Logs a student action inside a course.
    """
    activity = Activity(
        user_id=data.user_id,
        course_id=data.course_id,
        module_id=data.module_id,
        content_id=data.content_id,
        action=data.action
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


def get_student_activity(db: Session, user_id: int):
    """
    Returns all activity logs for a given student.
    """
    logs = (
        db.query(Activity)
        .filter(Activity.user_id == user_id)
        .order_by(Activity.timestamp.desc())
        .all()
    )

    return logs
