from sqlalchemy.orm import Session
from app.models.document import Document

# ---------------------------------------------------------
# Create a new document metadata entry
# ---------------------------------------------------------
def create_document(db: Session, doc_id: str, title: str, category: str, filename: str):
    document = Document(
        id=doc_id,
        title=title,
        category=category,
        filename=filename
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

# ---------------------------------------------------------
# Get a document by ID
# ---------------------------------------------------------
def get_document(db: Session, doc_id: str):
    return db.query(Document).filter(Document.id == doc_id).first()

# ---------------------------------------------------------
# List all documents
# ---------------------------------------------------------
def list_documents(db: Session):
    return db.query(Document).all()
