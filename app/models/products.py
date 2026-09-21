from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False)

    # Price
    price_usd = Column(Float, nullable=False)

    # Billing period (e.g., one_time, 3_months)
    billing_period = Column(String(50), nullable=False)

    # Availability fields
    active = Column(Boolean, default=True)
    coming_soon = Column(Boolean, default=False)

    # Description
    description = Column(String(500), nullable=True)
