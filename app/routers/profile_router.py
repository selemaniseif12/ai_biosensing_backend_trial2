from fastapi import APIRouter
import psycopg2
import os

router = APIRouter(prefix="/app")

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

@router.get("/profile/image")
def get_profile_image():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT image_base64 FROM profile WHERE id = 1")
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row or not row[0]:
        return "ERROR: No image stored in database"

    return row[0]  # RAW BASE64 TEXT
