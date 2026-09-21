from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from app.services.api_key_service import create_api_key_for_customer

def create_customer(db: Session, payload: CustomerCreate):
    """Create a new customer and assign an API key."""
    customer = Customer(
        name=payload.name,
        email=payload.email,
        api_key=""  # temporary placeholder
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    # Generate and assign API key
    create_api_key_for_customer(db, customer)

    return customer
