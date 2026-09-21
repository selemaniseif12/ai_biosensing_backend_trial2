import csv
import os
from sqlalchemy import text
from app.db_core import engine, SessionLocal
from app.models.models import Virus


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "analyzer_v1")

DEVICES_CSV = os.path.join(DATA_DIR, "analyzer_v1_devices.csv")
OUTPUTS_CSV = os.path.join(DATA_DIR, "analyzer_v1_outputs.csv")


# ---------------------------------------------------------
# Initialize Database (Create Tables + Load CSV Data + Seed Virus Table)
# ---------------------------------------------------------
def initialize_database():

    # -----------------------------------------------------
    # 1. CREATE RAW TABLES + LOAD CSVs (your original logic)
    # -----------------------------------------------------
    with engine.begin() as conn:

        # Create devices table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS devices (
                device_id INTEGER PRIMARY KEY,
                frequency_mhz REAL,
                center_electrode_mm REAL,
                diameter_mm REAL,
                chromium_layer_nm REAL,
                gold_layer_nm REAL,
                thickness_mm REAL
            )
        """))

        # Create device_outputs table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS device_outputs (
                device_id INTEGER PRIMARY KEY,
                frequency_mhz REAL,
                delta_f_mhz REAL,
                delta_m_g_cm2 REAL,
                m_g REAL
            )
        """))

        # Load devices CSV
        if os.path.exists(DEVICES_CSV):
            with open(DEVICES_CSV, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    conn.execute(text("""
                        INSERT OR REPLACE INTO devices VALUES (
                            :device_id, :frequency, :center, :diameter,
                            :chromium, :gold, :thickness
                        )
                    """), {
                        "device_id": row["Device ID"],
                        "frequency": row["Frequency(MHz)"],
                        "center": row["Center Electrode (mm)"],
                        "diameter": row["Diameter (mm)"],
                        "chromium": row["Chromium Layer (nm)"],
                        "gold": row["Gold Layer (nm)"],
                        "thickness": row["Thickness (mm)"]
                    })

        # Load outputs CSV
        if os.path.exists(OUTPUTS_CSV):
            with open(OUTPUTS_CSV, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    conn.execute(text("""
                        INSERT OR REPLACE INTO device_outputs VALUES (
                            :device_id, :frequency, :delta_f, :delta_m, :m
                        )
                    """), {
                        "device_id": row["Device ID"],
                        "frequency": row["Frequency(MHz)"],
                        "delta_f": row["Delta_f(MHz)"],
                        "delta_m": row["Delta_m(gm/cm2)"],
                        "m": row["m(gm)"]
                    })

    print("Analyzer v1 database initialized successfully.")

    # -----------------------------------------------------
    # 2. SEED VIRUS TABLE (SQLAlchemy ORM)
    # -----------------------------------------------------
    db = SessionLocal()

    if db.query(Virus).count() == 0:
        viruses = [
            Virus(id=1, name="SARS-CoV-2", mass_fg=0.02, sensitivity_fg=1.23),
            Virus(id=2, name="Influenza", mass_fg=0.05, sensitivity_fg=1.23),
            Virus(id=3, name="RSV", mass_fg=0.03, sensitivity_fg=1.23)
        ]
        db.add_all(viruses)
        db.commit()
        print("Virus table seeded successfully.")

    db.close()
