import os
from fpdf import FPDF
from datetime import datetime


def create_receipt_pdf(receipt_data: dict):
    """
    Generate a PDF receipt and return the file path.
    """

    # Ensure receipts folder exists
    receipts_folder = "receipts"
    os.makedirs(receipts_folder, exist_ok=True)

    # File name
    filename = f"receipt_{receipt_data['session_id']}.pdf"
    file_path = os.path.join(receipts_folder, filename)

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Payment Receipt", ln=True, align="C")
    pdf.ln(10)

    # Metadata
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Session ID: {receipt_data['session_id']}", ln=True)
    pdf.cell(200, 10, txt=f"User ID: {receipt_data['user_id']}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {receipt_data['created_at']}", ln=True)
    pdf.ln(10)

    # Items header
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Purchased Items:", ln=True)
    pdf.ln(5)

    # Items list
    pdf.set_font("Arial", size=12)
    for item in receipt_data["items"]:
        line = f"{item['name']} (x{item['quantity']}) - ${item['amount']:.2f}"
        pdf.cell(200, 8, txt=line, ln=True)

    pdf.ln(10)

    # Total
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt=f"Total: ${receipt_data['total']:.2f}", ln=True)

    # Save PDF
    pdf.output(file_path)

    return file_path
