import os
from fastapi.responses import FileResponse

# Always resolve absolute path, regardless of working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DOCS_PATH = os.path.join(BASE_DIR, "..", "docs_content")

BASE_DOCS_PATH = os.path.abspath(BASE_DOCS_PATH)

def load_pdf(filename: str):
    file_path = os.path.join(BASE_DOCS_PATH, filename)

    if not os.path.exists(file_path):
        return None

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=filename
    )
