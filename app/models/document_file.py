from sqlalchemy import Column, Integer, String, LargeBinary
from app.database import Base

class DocumentFile(Base):
    __tablename__ = "document_files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    content = Column(LargeBinary)  # PDF stored as binary
