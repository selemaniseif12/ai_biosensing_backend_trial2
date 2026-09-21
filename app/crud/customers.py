from sqlalchemy.orm import Session
from app.models.customer import Customer


from app.schemas.customer import CustomerCreate, CustomerUpdate


def create_customer(db: Session, customer_data: CustomerCreate):
    customer = Customer(
        name=customer_data.name,
        email=customer_data.email,
        organization=customer_data.organization,
        phone=customer_data.phone,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()


def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_all_customers(db: Session):
    return db.query(Customer).all()


def update_customer(db: Session, customer_id: int, update_data: CustomerUpdate):
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        return None

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int):
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        return False

    db.delete(customer)
    db.commit()
    return True
