import csv
from app.db_core import SessionLocal
from app.models.models import Analyzer1Device

def load_devices():
    db = SessionLocal()

    with open("data/analyzer_v1/analyzer_v1_devices.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            device = Analyzer1Device(
                device_id=int(row["Device ID"]),
                frequency_mhz=float(row["Frequency(MHz)"]),
                center_electrode_mm=float(row["Center Electrode (mm)"]),
                diameter_mm=float(row["Diameter (mm)"]),
                chromium_nm=float(row["Chromium Layer (nm)"]),
                gold_nm=float(row["Gold Layer (nm)"]),
                thickness_mm=float(row["Thickness (mm)"]),
                delta_f_mhz=None,
                m_g=None
            )
            db.add(device)

    db.commit()
    db.close()
    print("Devices loaded successfully.")

if __name__ == "__main__":
    load_devices()
