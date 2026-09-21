from app.models.virus import Virus
from app.database import SessionLocal

db = SessionLocal()

v = Virus(id=1, name="Test Virus", mass_fg=12.5)
db.add(v)
db.commit()

print("Inserted into REAL DB:", db.bind.url)

db.close()

