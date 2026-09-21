import os
import importlib

try:
    sqlalchemy = importlib.import_module("sqlalchemy")
    sqlalchemy_orm = importlib.import_module("sqlalchemy.orm")
except ModuleNotFoundError as exc:
    if exc.name and exc.name.startswith("sqlalchemy"):
        raise RuntimeError(
            "SQLAlchemy is required. Install it with: pip install sqlalchemy"
        ) from exc
    raise

create_engine = sqlalchemy.create_engine
sessionmaker = sqlalchemy_orm.sessionmaker
declarative_base = sqlalchemy_orm.declarative_base

# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------
def load_env_file(path=".env"):
    """Load simple KEY=VALUE entries without requiring python-dotenv."""
    if not os.path.isfile(path):
        return

    with open(path, encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("\"'"))

load_env_file()

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

    from .models.token_model import TokenModel
    from .models.consulting_model import ConsultingRequestModel
    from .models.service_model import Service
    from .models.receipt import Receipt
    from .models.cart_item import CartItem
    from .models.products import Product   # ⭐ FIXED MODEL NAME

    # No Base.metadata.create_all()
    # No Base.metadata.drop_all()
    # Production stays safe.


# ---------------------------------------------------------
# DEVELOPMENT-ONLY: Auto-create tables if missing
# ---------------------------------------------------------
ENV = os.getenv("ENV", "production").lower()

if ENV == "development":
    try:
        from .models.products import Product
        from .models.cart_item import CartItem

        Base.metadata.create_all(bind=engine)
        print("Development mode: tables auto-created.")
    except Exception as e:
        print("Table creation skipped:", e)
else:
    print("Production mode: table auto-creation disabled.")
