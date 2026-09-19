from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import os

from app.dependencies import get_db
from app.crud.document_crud import get_document, list_documents
from app.utils.pdf_loader import load_pdf

router = APIRouter(
    prefix="/docs",
    tags=["Documents"]   # ⭐ FIXED: unified tag to remove Swagger duplication
)

# ---------------------------------------------------------
# List all documents (metadata only)
# ---------------------------------------------------------
@router.get("/list")
def list_all_documents(db: Session = Depends(get_db)):
    docs = list_documents(db)

    if not isinstance(docs, list):
        raise HTTPException(status_code=500, detail="Invalid document list format")

    return [
        {
            "id": doc.id,
            "title": doc.title,
            "category": doc.category,
            "filename": doc.filename
        }
        for doc in docs
    ]

# ---------------------------------------------------------
# Serve raw PDF files by filename
# ---------------------------------------------------------
DOCS_FOLDER = "app/docs_content"

@router.get("/file/{filename}")
def get_pdf_by_filename(filename: str):
    file_path = os.path.join(DOCS_FOLDER, filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"PDF file '{filename}' not found in docs_content folder"
        )

    return FileResponse(file_path, media_type="application/pdf")

# ---------------------------------------------------------
# Get a specific document by ID (DB lookup)
# ---------------------------------------------------------
@router.get("/{doc_id:path}")
def get_document_file(doc_id: str, db: Session = Depends(get_db)):
    document = get_document(db, doc_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    pdf_response = load_pdf(document.filename)

    if not pdf_response:
        raise HTTPException(
            status_code=404,
            detail=f"PDF file '{document.filename}' missing in docs_content folder"
        )

    return pdf_response
