from app.models.virus import Virus
from app.database import SessionLocal

def seed():
    db = SessionLocal()

    # Check if virus exists
    existing = db.query(Virus).filter(Virus.id == 1).first()
    if existing:
        print("Virus already exists:", existing.name)
        db.close()
        return

    # Insert virus
    v = Virus(id=1, name="Test Virus", mass_fg=12.5)
    db.add(v)
    db.commit()
    db.close()

    print("Virus inserted successfully.")

if __name__ == "__main__":
    seed()
