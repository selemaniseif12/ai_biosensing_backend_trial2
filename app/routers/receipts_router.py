import logging
import textwrap
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.payment_receipt import PaymentReceipt
from app.models.user import User


logger = logging.getLogger(__name__)

receipts_router = APIRouter(
    prefix="/receipts",
    tags=["Receipts"],
)


# ---------------------------------------------------------
# COMPANY INFORMATION
# ---------------------------------------------------------

COMPANY_NAME = "Piezo Pico to Femtotechnology Sensors Inc."
COMPANY_ADDRESS = "303-10702 99AVE, Morinville, AB, Canada"
COMPANY_EMAIL = "selemaniseif1974@gmail.com"
COMPANY_PHONE = "+1 (780) 604 4032"
COMPANY_GST = "GST: 123456789RT0001"


# ---------------------------------------------------------
# RECEIPT SERIALIZATION HELPERS
# ---------------------------------------------------------

def get_receipt_items(items):
    """
    Convert stored item descriptions to a list.

    Supports the semicolon-delimited format used by the updated
    Stripe Checkout webhook and older comma-delimited receipts.
    """

    if not items:
        return []

    if "; " in items:
        return [
            item.strip()
            for item in items.split("; ")
            if item.strip()
        ]

    if "," in items:
        return [
            item.strip()
            for item in items.split(",")
            if item.strip()
        ]

    return [items.strip()] if items.strip() else []


def serialize_receipt(receipt: PaymentReceipt) -> dict:
    """Return the public representation of a payment receipt."""

    return {
        "receipt_id": receipt.id,
        "invoice_number": receipt.invoice_number,
        "service_name": receipt.service_name,
        "amount_paid": receipt.amount_paid,
        "currency": receipt.currency,
        "date": (
            receipt.created_at.isoformat()
            if receipt.created_at
            else None
        ),
        "items": get_receipt_items(receipt.items),
    }


def get_owned_receipt(
    db: Session,
    receipt_id: int,
    user_id: int,
) -> PaymentReceipt:
    """
    Find a receipt belonging to the authenticated customer.

    Return the same 404 response for missing receipts and receipts
    owned by someone else.
    """

    receipt = (
        db.query(PaymentReceipt)
        .filter(
            PaymentReceipt.id == receipt_id,
            PaymentReceipt.user_id == user_id,
        )
        .first()
    )

    if not receipt:
        raise HTTPException(
            status_code=404,
            detail="Receipt not found.",
        )

    return receipt


# ---------------------------------------------------------
# LIST THE AUTHENTICATED CUSTOMER'S RECEIPTS
# ---------------------------------------------------------

@receipts_router.get("/list")
def list_receipts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List receipts belonging to the authenticated customer.

    The customer ID comes from the verified JWT, not a query
    parameter supplied by the browser.
    """

    receipts = (
        db.query(PaymentReceipt)
        .filter(PaymentReceipt.user_id == current_user.id)
        .order_by(PaymentReceipt.created_at.desc())
        .all()
    )

    return {
        "receipts": [
            serialize_receipt(receipt)
            for receipt in receipts
        ]
    }


# ---------------------------------------------------------
# RECEIPT DETAILS
# ---------------------------------------------------------

@receipts_router.get("/detail/{receipt_id}")
def receipt_detail(
    receipt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return receipt details only to the receipt's owner."""

    receipt = get_owned_receipt(
        db=db,
        receipt_id=receipt_id,
        user_id=current_user.id,
    )

    result = serialize_receipt(receipt)

    # Expose the PaymentIntent identifier only to the receipt owner.
    result["stripe_payment_intent_id"] = (
        receipt.stripe_payment_intent_id
    )

    return result


# ---------------------------------------------------------
# PDF GENERATOR
# ---------------------------------------------------------

def _escape_pdf_text(value) -> str:
    """
    Prepare text for a PDF literal string using a standard font.

    Unsupported characters are replaced rather than causing
    Latin-1 encoding failures.
    """

    text = str(value or "")
    text = text.encode("latin-1", errors="replace").decode("latin-1")

    return (
        text.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("\r", " ")
        .replace("\n", " ")
    )


def generate_simple_pdf(receipt: PaymentReceipt) -> BytesIO:
    """
    Generate a simple, single-page PDF receipt.

    Object offsets are calculated from the final byte buffer so
    the PDF cross-reference table is valid.
    """

    created_at = (
        receipt.created_at.strftime("%Y-%m-%d %H:%M:%S")
        if receipt.created_at
        else "Unavailable"
    )

    currency = (receipt.currency or "usd").upper()

    lines = [
        f"Invoice: {receipt.invoice_number or receipt.id}",
        f"Date: {created_at}",
        "",
        "Company:",
        COMPANY_NAME,
        COMPANY_ADDRESS,
        COMPANY_EMAIL,
        COMPANY_PHONE,
        COMPANY_GST,
        "",
        f"Service: {receipt.service_name or 'Purchase'}",
        f"Amount: {receipt.amount_paid or 0:.2f} {currency}",
        "",
        "Items:",
        receipt.items or "No item details recorded.",
        "",
        "Thank you for your business.",
    ]

    # Wrap long lines to fit within the page width.
    wrapped_lines = []

    for line in lines:
        if not line:
            wrapped_lines.append("")
        else:
            wrapped_lines.extend(
                textwrap.wrap(
                    line,
                    width=85,
                    replace_whitespace=True,
                    drop_whitespace=True,
                    break_long_words=True,
                    break_on_hyphens=False,
                ) or [""]
            )

    # Build the page's text stream.
    commands = [
        "BT",
        "/F1 10 Tf",
        "50 750 Td",
    ]

    for index, line in enumerate(wrapped_lines):
        if index:
            commands.append("0 -14 Td")

        commands.append(f"({_escape_pdf_text(line)}) Tj")

    commands.append("ET")

    content_bytes = "\n".join(commands).encode("latin-1")

    # PDF objects use one-based object numbers.
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            b"<< /Type /Page /Parent 2 0 R "
            b"/MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 4 0 R >> >> "
            b"/Contents 5 0 R >>"
        ),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        (
            f"<< /Length {len(content_bytes)} >>\n".encode("ascii")
            + b"stream\n"
            + content_bytes
            + b"\nendstream"
        ),
    ]

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]

    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))

        pdf.extend(f"{index} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)

    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")

    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))

    pdf.extend(
        (
            f"trailer\n"
            f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n"
            f"%%EOF\n"
        ).encode("ascii")
    )

    buffer = BytesIO(bytes(pdf))
    buffer.seek(0)

    return buffer


# ---------------------------------------------------------
# DOWNLOAD A RECEIPT PDF
# ---------------------------------------------------------

@receipts_router.get("/pdf/{receipt_id}")
def receipt_pdf(
    receipt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Download a PDF only if the receipt belongs to the customer."""

    receipt = get_owned_receipt(
        db=db,
        receipt_id=receipt_id,
        user_id=current_user.id,
    )

    pdf_buffer = generate_simple_pdf(receipt)

    filename = f"receipt_{receipt.invoice_number or receipt.id}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            ),
            "Cache-Control": "no-store",
        },
    )


# ---------------------------------------------------------
# ROUTER INITIALIZER
# ---------------------------------------------------------

def init_receipts(app):
    app.include_router(receipts_router)