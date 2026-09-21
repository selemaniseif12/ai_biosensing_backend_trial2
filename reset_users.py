from app.models.database import SessionLocal
from app.models.models import User

def reset_users():
    db = SessionLocal()
    try:
        deleted = db.query(User).delete()
        db.commit()
        print(f"Deleted {deleted} users.")
    except Exception as e:
        print("Error:", e)
    finally:
        db.close()

if __name__ == "__main__":
    reset_users()
