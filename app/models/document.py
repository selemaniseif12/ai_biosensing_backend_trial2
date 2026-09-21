from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)          # e.g. "payment_system_architecture_docs"
    title = Column(String, nullable=False)                     # Human‑readable name
    category = Column(String, nullable=False)                  # e.g. "Architecture", "API", "Platform"
    filename = Column(String, nullable=False)                  # e.g. "payment_system_architecture.pdf"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
