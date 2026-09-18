from app.models.document_file import DocumentFile
from app.database import SessionLocal

def save_pdf_to_db(name: str, file_path: str):
    db = SessionLocal()
    with open(file_path, "rb") as f:
        content = f.read()

    doc = db.query(DocumentFile).filter(DocumentFile.name == name).first()
    if doc:
        doc.content = content
    else:
        doc = DocumentFile(name=name, content=content)
        db.add(doc)

    db.commit()
    db.close()
