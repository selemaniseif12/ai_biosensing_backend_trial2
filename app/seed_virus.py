from app.models.virus import Virus
from app.database import SessionLocal

def seed_virus():
    db = SessionLocal()

    # Check if virus already exists
    existing = db.query(Virus).filter(Virus.id == 1).first()
    if existing:
        print("Virus with ID 1 already exists:", existing.name)
        db.close()
        return

    # Insert new virus
    v = Virus(
        id=1,
        name="Test Virus",
        mass_fg=12.5
    )

    db.add(v)
    db.commit()
    db.close()

    print("Virus inserted successfully.")

if __name__ == "__main__":
    seed_virus()
