from .analyzer_v2_loader import AnalyzerV2Loader

class AnalyzerV2:
    def __init__(self):
        loader = AnalyzerV2Loader().load()
        self.table_2a = loader.table_2a
        self.table_2b = loader.table_2b
        self.joined   = loader.joined

    def get_sample(self, sample_id: int):
        row = self.joined[self.joined["ID"] == sample_id]
        if row.empty:
            return None
        return row.to_dict(orient="records")[0]

    def list_all(self):
        return self.joined.to_dict(orient="records")

    def get_by_ion(self, ion: str):
        df = self.joined[self.joined["Ion/Analyte"] == ion]
        return df.to_dict(orient="records")

    def compute_mass(self, sample_id: int):
        """
        Uses Δm = (Δf / f) * m
        """
        row = self.table_2b[self.table_2b["ID"] == sample_id]
        if row.empty:
            return None

        delta_f = float(row["Delta_f_MHz"])
        f = float(row["Frequency_f2_MHz"])
        m = float(row["Electrode_Mass_m_g"])

        delta_m = (delta_f / f) * m
        return {
            "ID": sample_id,
            "delta_m_computed": delta_m
        }
