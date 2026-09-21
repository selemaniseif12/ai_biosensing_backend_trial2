from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.models.database import SessionLocal   # <-- FIXED


class AnalyticsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        db: Session = SessionLocal()

        try:
            response = await call_next(request)
            return response
        finally:
            db.close()
