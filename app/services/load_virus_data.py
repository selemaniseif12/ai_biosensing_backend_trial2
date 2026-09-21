import csv
from pathlib import Path
from sqlalchemy.orm import Session

from app.models.virus import Virus
from app.models.device import Device







# Correct folder containing your CSVs
DATA_DIR = Path(__file__).resolve().parent.parent / "ml" / "virus_tables"

DEVICE_FILES = [
    DATA_DIR / "device1a.csv",
    DATA_DIR / "device1b.csv",
    DATA_DIR / "device1c.csv",
    DATA_DIR / "device1d.csv",
    DATA_DIR / "device1e.csv",
    DATA_DIR / "device2.csv",
    DATA_DIR / "device3.csv",
    DATA_DIR / "device4.csv",
    DATA_DIR / "device5.csv",
]

VIRUS_MASTER_FILE = DATA_DIR / "virus_master.csv"


def normalize_key(key: str) -> str:
    """Normalize CSV header keys."""
    return (
        key.replace("\ufeff", "")
        .strip()
        .lower()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
    )


def load_virus_master(db: Session) -> None:
    if not VIRUS_MASTER_FILE.exists():
        print(f"[WARN] Virus master file not found: {VIRUS_MASTER_FILE}")
        return

    with VIRUS_MASTER_FILE.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            virus_id = int(row["id"])

            existing = db.query(Virus).filter(Virus.id == virus_id).first()
            if existing:
                continue

            virus = Virus(
                id=virus_id,
                name=row["name"],
                mass_fg=float(row["mass_fg"]),
                family=row.get("family"),
                description=row.get("description"),
            )
            db.add(virus)

    db.commit()
    print("[INFO] Virus master table loaded.")


def ensure_device_exists(db: Session, device_id: int) -> None:
    """Ensure device exists in DB with correct sensitivity."""
    existing = db.query(Device).filter(Device.id == device_id).first()
    if existing:
        return

    sensitivity_map = {
        1: 1200,
        2: 1.23,
        3: 900,
        4: 700,
        5: 500,
    }

    device = Device(
        id=device_id,
        sensitivity_fg=sensitivity_map.get(device_id, 1200),
    )
    db.add(device)
    db.commit()


def load_device_table(db: Session, path: Path) -> None:
    """
    Loads device CSV files.
    Ensures devices exist.
    Does NOT insert virus rows into Device table.
    """

    if not path.exists():
        print(f"[WARN] Device file not found: {path}")
        return

    with path.open("r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        print(f"[DEBUG] RAW HEADERS in {path.name}: {reader.fieldnames}")

        # Normalize headers
        normalized_headers = {normalize_key(k): k for k in reader.fieldnames}
        print(f"[DEBUG] NORMALIZED HEADERS in {path.name}: {normalized_headers}")

        def get(colname: str, row: dict):
            """Fetch a column regardless of formatting."""
            norm = normalize_key(colname)
            for nk, original in normalized_headers.items():
                if nk == norm:
                    return row[original]
            raise KeyError(
                f"Column '{colname}' not found. Normalized headers: {normalized_headers}"
            )

        for row in reader:
            # Read CSV fields (your actual headers)
            virus_id = int(get("virusid", row))          # Virus ID
            virus_name = get("virus", row)               # Virus name
            antibody = get("antibody", row)              # Antibody
            antigen = get("antigen", row)                # Antigen name
            antigen_mass_fg = float(get("massfg", row))  # mass_fg column
            device_id = int(get("deviceid", row))        # device_id
            device_sensitivity_fg = float(get("devicesensitivityfg", row))
            virus_count_original = float(get("viruscountoriginal", row))
            virus_count_computed = float(get("viruscountcomputed", row))

            # Ensure device exists
            ensure_device_exists(db, device_id)

            # DO NOT insert into Device table (model does not support these fields)
            # This loader only ensures devices exist and prints debug info.

        print(f"[INFO] Loaded device file: {path.name}")


def initialize_virus_data(db: Session) -> None:
    print("[INFO] Initializing virus data...")

    load_virus_master(db)

    for path in DEVICE_FILES:
        load_device_table(db, path)

    print("[INFO] All virus/device data loaded successfully.")
