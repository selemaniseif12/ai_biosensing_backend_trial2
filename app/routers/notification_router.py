from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.notification import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# ---------------------------------------------------------
# Create a notification
# ---------------------------------------------------------
@router.post("/")
def create_notification(user_id: int, message: str, db: Session = Depends(get_db)):
    note = Notification(user_id=user_id, message=message)
    db.add(note)
    db.commit()
    db.refresh(note)
    return {"message": "Notification created", "notification": note}


# ---------------------------------------------------------
# Get notifications for a user
# ---------------------------------------------------------
@router.get("/{user_id}")
def get_notifications(user_id: int, db: Session = Depends(get_db)):
    notes = db.query(Notification).filter(Notification.user_id == user_id).all()
    return notes


# ---------------------------------------------------------
# Mark notification as read
# ---------------------------------------------------------
@router.post("/{notification_id}/read")
def mark_read(notification_id: int, db: Session = Depends(get_db)):
    note = db.query(Notification).filter(Notification.id == notification_id).first()
    if not note:
        return {"error": "Notification not found"}

    note.is_read = True
    db.commit()
    return {"message": "Notification marked as read"}
