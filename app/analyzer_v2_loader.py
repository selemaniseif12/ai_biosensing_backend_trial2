import pandas as pd
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent / "data" / "analyzer_v2"

class AnalyzerV2Loader:
    def __init__(self):
        self.table_2a_path = BASE_PATH / "analyzer_v2_table_2a.csv"
        self.table_2b_path = BASE_PATH / "analyzer_v2_table_2b.csv"
        self.joined_path   = BASE_PATH / "analyzer_v2_joined.csv"

        self.table_2a = None
        self.table_2b = None
        self.joined   = None

    def load(self):
        # Load CSVs
        self.table_2a = pd.read_csv(self.table_2a_path)
        self.table_2b = pd.read_csv(self.table_2b_path)
        self.joined   = pd.read_csv(self.joined_path)

        # Clean ID column safely
        self.joined["ID"] = pd.to_numeric(self.joined["ID"], errors="coerce")
        self.joined = self.joined.dropna(subset=["ID"])
        self.joined["ID"] = self.joined["ID"].astype(int)

        return self
