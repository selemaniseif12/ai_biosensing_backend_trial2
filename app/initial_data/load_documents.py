from sqlalchemy.orm import Session
from app.crud.document_crud import create_document, get_document

# ---------------------------------------------------------
# Preload all documentation metadata into the database
# ---------------------------------------------------------
def load_initial_documents(db: Session):

    documents = [
        {
            "id": "backend_frontend_architecture_docs",
            "title": "Backend ↔ Frontend Architecture",
            "category": "Architecture",
            "filename": "backend_frontend_architecture.pdf"
        },
        {
            "id": "biosensing_platform_docs",
            "title": "Biosensing Platform Documentation",
            "category": "Platform",
            "filename": "biosensing_platform.pdf"
        },
        {
            "id": "course_outline_fullstack_api_engineering_docs",
            "title": "Fullstack API Engineering Course Outline",
            "category": "Course",
            "filename": "course_outline_fullstack_api_engineering.pdf"
        },
        {
            "id": "ml_models_folder_structure_docs",
            "title": "ML Models Folder Structure",
            "category": "Machine Learning",
            "filename": "ml_models_folder_structure.pdf"
        },
        {
            "id": "main_py_documentation_docs",
            "title": "main.py Documentation",
            "category": "Backend",
            "filename": "main_py_documentation.pdf"
        },
        {
            "id": "payment_system_architecture_docs",
            "title": "Payment System Architecture",
            "category": "Payments",
            "filename": "payment_system_architecture.pdf"
        },
        {
            "id": "router_documentation_docs",
            "title": "Router Documentation",
            "category": "Backend",
            "filename": "router_documentation.pdf"
        },
        {
            "id": "swagger_documentation_docs",
            "title": "Swagger Documentation",
            "category": "API",
            "filename": "swagger_documentation.pdf"
        }
    ]

    for doc in documents:
        # Skip if already exists
        existing = get_document(db, doc["id"])
        if existing:
            continue

        create_document(
            db=db,
            doc_id=doc["id"],
            title=doc["title"],
            category=doc["category"],
            filename=doc["filename"]
        )
