from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from app.database import SessionLocal
from app.models.models import GovernmentMessage
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

router = APIRouter(
    prefix="/api/government",
    tags=["Government"]
)

class GovernmentContact(BaseModel):
    organization: str
    department: str | None = None
    contactName: str
    email: str
    phone: str | None = None
    country: str | None = None
    message: str
    priority: str


def send_email_notifications(payload: GovernmentContact):
    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))

    # Admin email content
    admin_subject = f"New Government Contact Request — {payload.organization}"
    admin_body = f"""
A new government contact request has been submitted.

Organization: {payload.organization}
Department: {payload.department}
Name: {payload.contactName}
Email: {payload.email}
Phone: {payload.phone}
Country: {payload.country}
Priority: {payload.priority}

Message:
{payload.message}

Submitted at: {datetime.utcnow()}
"""

    # User confirmation email content
    user_subject = "Your Government Contact Request Has Been Received"
    user_body = f"""
Hello {payload.contactName},

Thank you for contacting Piezo-Pico to Femtotechnology Sensors Inc.
Your request has been received and our team will respond shortly.

Here is a copy of your submission:

Organization: {payload.organization}
Department: {payload.department}
Message: {payload.message}
Priority: {payload.priority}

Best regards,
Piezo-Pico to Femtotechnology Sensors Inc.
"""

    # Admin emails (send to both)
    admin_emails = [
        "selemaniseif12@yahoo.com",
        "selemaniseif1974@gmail.com"
    ]

    for admin_email in admin_emails:
        message = Mail(
            from_email="selemaniseif1974@gmail.com",  # VERIFIED SENDER
            to_emails=admin_email,
            subject=admin_subject,
            plain_text_content=admin_body
        )
        sg.send(message)

    # Send confirmation to user
    message_user = Mail(
        from_email="selemaniseif1974@gmail.com",  # VERIFIED SENDER
        to_emails=payload.email,
        subject=user_subject,
        plain_text_content=user_body
    )
    sg.send(message_user)


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

        # Send emails
        send_email_notifications(payload)

        return {"success": True, "id": new_msg.id}

    except Exception as e:
        print("🔥 GOVERNMENT INSERT OR EMAIL ERROR:", e)
        db.rollback()
        return {"success": False, "error": str(e)}

    finally:
        db.close()


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
        print("🔥 GOVERNMENT FETCH ERROR:", e)
        return {"success": False, "data": [], "error": str(e)}

    finally:
        db.close()
