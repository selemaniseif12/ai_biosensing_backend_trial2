import csv
import os

CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    "virus_multiclass.csv"
)

virus_names_175 = {}
virus_masses_175 = {}
virus_flow_rates_175 = {}
virus_antigens_175 = {}
virus_antibodies_175 = {}

def load_multiclass_metadata():
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                virus_id = int(row["virus_id"])
            except (ValueError, TypeError):
                # Skip malformed rows like '...' or empty lines
                continue

            virus_names_175[virus_id] = row.get("name")
            virus_masses_175[virus_id] = float(row.get("mass_fg", 0))
            virus_flow_rates_175[virus_id] = float(row.get("flow_rate", 0))
            virus_antigens_175[virus_id] = row.get("antigen")
            virus_antibodies_175[virus_id] = row.get("antibody")

load_multiclass_metadata()
