import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.document_file import DocumentFile
from app.database import Base

# 1. REAL Neon connection URL
NEON_URL = "postgresql+psycopg2://neondb_owner:npg_Pp4QjJzMRUH3@ep-royal-haze-a5hy0nay-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(NEON_URL)
SessionLocal = sessionmaker(bind=engine)

# 2. Folder containing your PDFs
DOCS_FOLDER = "app/docs_content"

def migrate_all_pdfs():
    db = SessionLocal()

    # Ensure table exists
    Base.metadata.create_all(bind=engine)

    # Loop through all files in docs_content
    for filename in os.listdir(DOCS_FOLDER):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(DOCS_FOLDER, filename)

            # Remove .pdf extension for DB name
            doc_name = filename.replace(".pdf", "")

            print(f"Uploading: {filename} as {doc_name}")

            with open(file_path, "rb") as f:
                content = f.read()

            # Check if document already exists
            existing = db.query(DocumentFile).filter(DocumentFile.name == doc_name).first()

            if existing:
                existing.content = content
            else:
                new_doc = DocumentFile(name=doc_name, content=content)
                db.add(new_doc)

            db.commit()

    db.close()
    print("Migration completed successfully.")

if __name__ == "__main__":
    migrate_all_pdfs()
