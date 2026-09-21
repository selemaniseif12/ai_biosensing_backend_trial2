from fastapi import FastAPI
from app.routers import analyze_v1, analyze_v2, customers, admin

app = FastAPI(
    title="AI Biosensing API",
    version="2.0.0",
)

app.include_router(analyze_v1.router)
app.include_router(analyze_v2.router)
app.include_router(customers.router)
app.include_router(admin.router)

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

#!/bin/bash

PROJECT_ID="YOUR_PROJECT_ID"
SERVICE_NAME="biosensing-api"

gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080

#!/bin/bash

gcloud sql instances create biosensing-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1

import secrets

def generate_api_key():
    return secrets.token_hex(32)

1. Admin creates customer
2. Customer receives API key
3. Customer logs into portal
4. Customer tests /v1/analyze
5. Customer upgrades plan

✔ HTTPS enabled
✔ Cloud Run auto-scaling
✔ Cloud SQL connected
✔ API Gateway rate limiting
✔ Logging + Monitoring
✔ Error reporting
✔ Versioning (/v1, /v2)
✔ Backups enabled
