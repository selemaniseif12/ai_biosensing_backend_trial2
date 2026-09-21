# FILE: app/models/payment_receipt.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

class PaymentReceipt(Base):
    __tablename__ = "payment_receipts"

    id = Column(Integer, primary_key=True, index=True)

    # Human‑friendly invoice number, e.g. INV-2026-0001
    invoice_number = Column(String, unique=True, index=True)

    # Link to the user who paid
    user_id = Column(Integer, index=True)

    # What the payment was for (Consulting, Course, Store, etc.)
    service_name = Column(String)

    # Amount paid
    amount_paid = Column(Float)

    # Currency, e.g. "cad"
    currency = Column(String, default="cad")

    # When the receipt was created
    created_at = Column(DateTime, default=datetime.utcnow)

    # Simple description or comma‑separated items
    items = Column(String)

    # Stripe payment intent ID for traceability
    stripe_payment_intent_id = Column(String, index=True)
