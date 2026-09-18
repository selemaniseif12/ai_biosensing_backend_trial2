from fastapi import APIRouter, Response, HTTPException
from app.database import SessionLocal
from app.models.document_file import DocumentFile

router = APIRouter(
    prefix="/docs",
    tags=["Documentation"]
)

# ---------------------------------------------------------
# NEW: List all documents from Neon (correct table)
# ---------------------------------------------------------
@router.get("/list")
def list_all_documents():
    db = SessionLocal()
    docs = db.query(DocumentFile).all()
    db.close()

    return [
        {
            "id": doc.id,
            "name": doc.name,
            "title": doc.title if hasattr(doc, "title") else doc.name,
            "category": doc.category if hasattr(doc, "category") else "General"
        }
        for doc in docs
    ]

# ---------------------------------------------------------
# NEW: Serve raw PDF files from Neon (correct system)
# ---------------------------------------------------------
@router.get("/{name}")
def get_document(name: str):
    db = SessionLocal()
    doc = db.query(DocumentFile).filter(DocumentFile.name == name).first()
    db.close()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return Response(content=doc.content, media_type="application/pdf")
