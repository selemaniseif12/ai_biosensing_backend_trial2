import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Add it in your .env file.")

# ---------------------------------------------------------
# SQLAlchemy Engine (Neon PostgreSQL)
# ---------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# ---------------------------------------------------------
# Session Factory
# ---------------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ---------------------------------------------------------
# Base Model
# ---------------------------------------------------------
Base = declarative_base()

# ---------------------------------------------------------
# FastAPI Dependency
# ---------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------
# Register models ONLY — DO NOT CREATE TABLES (Production Safe)
# ---------------------------------------------------------
def init_db():
    """
    Import models so SQLAlchemy registers them.
    DO NOT create or modify tables in production.
    """

    from app.models.token_model import TokenModel
    from app.models.consulting_model import ConsultingRequestModel
    from app.models.service_model import Service
    from app.models.receipt import Receipt
    from app.models.cart_item import CartItem
    from app.models.products import Product   # ⭐ FIXED MODEL NAME

    # No Base.metadata.create_all()
    # No Base.metadata.drop_all()
    # Production stays safe.


# ---------------------------------------------------------
# DEVELOPMENT-ONLY: Auto-create tables if missing
# ---------------------------------------------------------
try:
    from app.models.products import Product   # ⭐ FIXED
    from app.models.cart_item import CartItem

    Base.metadata.create_all(bind=engine)
except Exception as e:
    print("Table creation skipped:", e)
