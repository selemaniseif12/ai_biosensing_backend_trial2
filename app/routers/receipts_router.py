# FILE: app/routers/receipts_router.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO

from app.database import get_db
from app.models.payment_receipt import PaymentReceipt

receipts_router = APIRouter(prefix="/receipts", tags=["Receipts"])

# -----------------------------
# Company Information
# -----------------------------
COMPANY_NAME = "Piezo Pico to Femtotechnology Sensors Inc."
COMPANY_ADDRESS = "303-10702 99AVE, Morinville, AB, Canada"
COMPANY_EMAIL = "selemaniseif1974@gmail.com"
COMPANY_PHONE = "+1 (780) 604 4032"
COMPANY_GST = "GST: 123456789RT0001"


# -----------------------------
# List Receipts
# -----------------------------
@receipts_router.get("/list")
def list_receipts(user_id: int, db: Session = Depends(get_db)):
    receipts = (
        db.query(PaymentReceipt)
        .filter(PaymentReceipt.user_id == user_id)
        .order_by(PaymentReceipt.created_at.desc())
        .all()
    )

    return {
        "receipts": [
            {
                "receipt_id": r.id,
                "invoice_number": r.invoice_number,
                "service_name": r.service_name,
                "amount_paid": r.amount_paid,
                "currency": r.currency,
                "date": r.created_at.isoformat(),
                "items": r.items.split(",") if r.items else [],
            }
            for r in receipts
        ]
    }


# -----------------------------
# Receipt Details
# -----------------------------
@receipts_router.get("/detail/{receipt_id}")
def receipt_detail(receipt_id: int, db: Session = Depends(get_db)):
    r = db.query(PaymentReceipt).filter(PaymentReceipt.id == receipt_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Receipt not found")

    return {
        "receipt_id": r.id,
        "invoice_number": r.invoice_number,
        "service_name": r.service_name,
        "amount_paid": r.amount_paid,
        "currency": r.currency,
        "date": r.created_at.isoformat(),
        "items": r.items.split(",") if r.items else [],
        "stripe_payment_intent_id": r.stripe_payment_intent_id,
    }


# -----------------------------
# Simple PDF Generator (No external libraries)
# -----------------------------
def generate_simple_pdf(receipt):
    buffer = BytesIO()

    # Minimal PDF header
    pdf = "%PDF-1.4\n"
    objects = []
    xref_positions = []

    def add_object(content):
        pos = len(pdf.encode("latin1"))
        xref_positions.append(pos)
        obj = f"{len(xref_positions)} 0 obj\n{content}\nendobj\n"
        return obj

    # Page content (simple text)
    text = f"""
Invoice: {receipt.invoice_number}
Date: {receipt.created_at.strftime('%Y-%m-%d %H:%M:%S')}
User ID: {receipt.user_id}

Company:
{COMPANY_NAME}
{COMPANY_ADDRESS}
{COMPANY_EMAIL}
{COMPANY_PHONE}
{COMPANY_GST}

Service: {receipt.service_name}
Amount: {receipt.amount_paid:.2f} {receipt.currency.upper()}

Items:
{receipt.items}

Thank you for your business.
"""

    # PDF text stream
    stream = f"<< /Length {len(text)} >>\nstream\n{text}\nendstream"
    objects.append(add_object(stream))

    # Page object
    page = "<< /Type /Page /Parent 2 0 R /Contents 1 0 R >>"
    objects.append(add_object(page))

    # Pages object
    pages = "<< /Type /Pages /Kids [2 0 R] /Count 1 >>"
    objects.append(add_object(pages))

    # Catalog
    catalog = "<< /Type /Catalog /Pages 3 0 R >>"
    objects.append(add_object(catalog))

    # Build PDF
    for obj in objects:
        pdf += obj

    # XREF table
    xref_start = len(pdf.encode("latin1"))
    pdf += "xref\n0 {}\n0000000000 65535 f \n".format(len(objects) + 1)

    for pos in xref_positions:
        pdf += f"{pos:010} 00000 n \n"

    # Trailer
    pdf += f"trailer\n<< /Size {len(objects)+1} /Root 4 0 R >>\nstartxref\n{xref_start}\n%%EOF"

    buffer.write(pdf.encode("latin1"))
    buffer.seek(0)
    return buffer


# -----------------------------
# PDF Endpoint
# -----------------------------
@receipts_router.get("/pdf/{receipt_id}")
def receipt_pdf(receipt_id: int, db: Session = Depends(get_db)):
    r = db.query(PaymentReceipt).filter(PaymentReceipt.id == receipt_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Receipt not found")

    pdf_buffer = generate_simple_pdf(r)
    filename = f"receipt_{r.invoice_number}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


# -----------------------------
# Router Initializer
# -----------------------------
def init_receipts(app):
    app.include_router(receipts_router)
