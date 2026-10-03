from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

# Correct imports for your project structure
from app.database import SessionLocal
from app.models.models import GovernmentMessage

router = APIRouter(
    prefix="/api/government",
    tags=["Government"]
)

# ⭐ Request model for government contact form
class GovernmentContact(BaseModel):
    organization: str
    department: str | None = None
    contactName: str
    email: str
    phone: str | None = None
    country: str | None = None
    message: str
    priority: str


# ⭐ POST — Submit Government Contact Form
@router.post("/contact")
def submit_government_contact(payload: GovernmentContact):
    db = SessionLocal()

    try:
        new_msg = GovernmentMessage(
            organization=payload.organization,
            department=payload.department,
            contactName=payload.contactName,
            email=payload.email,
            phone=payload.phone,
            country=payload.country,
            message=payload.message,
            priority=payload.priority,
            createdAt=datetime.utcnow()
        )

        db.add(new_msg)
        db.commit()
        db.refresh(new_msg)

        return {"success": True, "id": new_msg.id}

    except Exception as e:
        print("Government contact error:", e)
        db.rollback()
        return {"success": False}

    finally:
        db.close()


# ⭐ GET — Admin Viewer: Fetch All Government Messages
@router.get("/all")
def get_all_government_messages():
    db = SessionLocal()

    try:
        messages = (
            db.query(GovernmentMessage)
            .order_by(GovernmentMessage.createdAt.desc())
            .all()
        )

        return {"success": True, "data": messages}

    except Exception as e:
        print("Government fetch error:", e)
        return {"success": False, "data": []}

    finally:
        db.close()
