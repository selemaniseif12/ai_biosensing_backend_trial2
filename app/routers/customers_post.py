# app/routers/customers_post.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.database import Base, engine, SessionLocal

from app.models.models import User

router = APIRouter(prefix="/customers", tags=["Customers"])

class CustomerCreate(BaseModel):
    email: str
    full_name: str | None = None
    password: str
    role: str | None = "customer"

@router.post("/")
def create_customer(customer: CustomerCreate):
    db = SessionLocal()
    try:
        new_user = User(
            email=customer.email,
            full_name=customer.full_name,
            password=customer.password,   # You may hash later
            role=customer.role,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "Customer created successfully",
            "customer": {
                "id": new_user.id,
                "email": new_user.email,
                "full_name": new_user.full_name,
                "role": new_user.role,
            },
        }
    finally:
        db.close()
