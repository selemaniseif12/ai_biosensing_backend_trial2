from sqlalchemy.orm import Session
from app.models.customer import Customer



def create_customer(customer_data, db: Session):
    customer = Customer(
        name=customer_data.name,
        email=customer_data.email,
        phone=customer_data.phone,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_customer(customer_id: int, db: Session):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_all_customers(db: Session):
    return db.query(Customer).all()


def update_customer(customer_id: int, customer_data, db: Session):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return None

    customer.name = customer_data.name
    customer.email = customer_data.email
    customer.phone = customer_data.phone

    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(customer_id: int, db: Session):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return None

    db.delete(customer)
    db.commit()
    return {"deleted": True}
