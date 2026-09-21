# app/models/receipt.py

from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from app.database import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)

    # User who made the purchase
    user_id = Column(Integer, index=True, nullable=False)

    # Name of the purchased service (ml_v6, ml_v2, virus_access, etc.)
    service_name = Column(String, nullable=False)

    # Total amount paid in USD
    amount_paid = Column(Float, nullable=False)

    # Stripe or payment transaction ID
    transaction_id = Column(String, nullable=False)

    # Token issued for the purchased service
    token_issued = Column(String, nullable=False)

    # Timestamp of purchase
    date = Column(DateTime, default=datetime.utcnow)

    # Optional: JSON string of purchased items (if store has multiple items)
    items_json = Column(String, nullable=True)
