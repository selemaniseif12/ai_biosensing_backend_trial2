from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "local"
    PROJECT_NAME: str = "QCM AI Biosensing API"

    # Database (internal DB settings)
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_USER: str = "qcm_user"
    DB_PASSWORD: str = "qcm_password"
    DB_NAME: str = "qcm_biosensing"

    # Security
    JWT_SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # API keys
    ROOT_ADMIN_API_KEY: str = "CHANGE_ME_ADMIN_KEY"

    # ML
    MODEL_DIR: str = "models"
    DEFAULT_MODEL_NAME: str = "qcm_rf_model.pkl"

    # External services (must match your .env)
    AZURE_CLIENT_ID: str | None = None
    AZURE_CLIENT_SECRET: str | None = None
    AZURE_TENANT_ID: str | None = None

    STRIPE_SECRET_KEY: str | None = None
    STRIPE_WEBHOOK_SECRET: str | None = None

    DATABASE_URL: str | None = None

    # ⭐ ML model URLs (required to stop ValidationError)
    VIRUS_CLASSIFIER_URL: str | None = None
    VIRUS_MULTICLASS_V7_URL: str | None = None
    SPECTRAL_MODEL_URL: str | None = None
    RF_MODEL_URL: str | None = None
    SCALER_URL: str | None = None

    # ⭐ Pydantic v2 configuration (replaces old Config class)
    model_config = {
        "extra": "ignore",
        "env_file": ".env",
        "case_sensitive": True
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

# Stripe price IDs
STRIPE_PRICE_IDS = {
    "consulting_fixed": "price_1U2bYWBBErGCNvV44HTOR5ml",
    "consulting_custom": "price_1U2bc0BBErGCNvV40uAmvWHa",
    "course_biosensing_intro": "price_1U2bjZBBErGCNvV4eDZMAacR",
    "course_ml_v2": "price_1U2bmYBBErGCNvV49lpaDP9Z",
    "course_ml_v6": "price_1U2cHcBBErGCNvV4kZev14rV",
    "course_full_stack": "price_1U2bs5BBErGCNvV4nqbNa7qL",
    "model_access_v2": "price_1U2buABBErGCNvV4Hjy7c0yw",
    "model_access_v6": "price_1U2bwmBBErGCNvV4Y5sqt3Yp",
    "bundle_v2_v6": "price_1U2c3cBBErGCNvV4H8x8MCON",
    "virus_db_sub": "price_1U2c60BBErGCNvV4sTQrLZRb",
    "device_low_grade": "price_1U2cBABBErGCNvV4bRRgpzkX"
}
