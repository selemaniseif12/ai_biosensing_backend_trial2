from fastapi import APIRouter, Response
from app.database import SessionLocal
from app.models.document_file import DocumentFile

router = APIRouter()

@router.get("/docs/{name}")
def get_document(name: str):
    db = SessionLocal()
    doc = db.query(DocumentFile).filter(DocumentFile.name == name).first()
    db.close()

    if not doc:
        return {"error": "Document not found"}

    return Response(content=doc.content, media_type="application/pdf")
