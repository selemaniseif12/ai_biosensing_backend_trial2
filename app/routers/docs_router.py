from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter(
    prefix="/docs",
    tags=["Documents"]
)

# ---------------------------------------------------------
# List all PDF documents from filesystem
# ---------------------------------------------------------
@router.get("/list")
def list_all_documents():
    folder = "./app/docs_content"
    files = os.listdir(folder)
    docs = []

    for f in files:
        if f.lower().endswith(".pdf"):
            docs.append({
                "id": f,
                "name": f,
                "title": f.replace("_", " ").replace(".pdf", "").title(),
                "category": "General"
            })

    return docs

# ---------------------------------------------------------
# Serve raw PDF files from filesystem
# ---------------------------------------------------------
DOCS_FOLDER = "./app/docs_content"

@router.get("/{name}")
def get_document(name: str):
    file_path = os.path.join(DOCS_FOLDER, name)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"PDF file '{name}' not found in docs_content folder"
        )

    return FileResponse(file_path, media_type="application/pdf")
