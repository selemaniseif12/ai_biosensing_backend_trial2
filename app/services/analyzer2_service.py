from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class Table2A:
    id: int
    ion: str
    mass_g: float | None
    concentration_m: float | None
    dilution_volume_ml: float
    f1_mhz: float


@dataclass
class Table2B:
    id: int
    af_mhz: float
    am_table: float
    m_g: float
    f2_mhz: float


# -----------------------------
# TABLE 2A — INPUT PARAMETERS
# -----------------------------
TABLE_2A: Dict[int, Table2A] = {
    1: Table2A(1, "Na+", 0.5, 0.12, 28.48, 1.693956482),
    2: Table2A(2, "K+", 0.5, 0.12, 28.48, 1.693956482),
    3: Table2A(3, "Ca2+", 0.5, 0.12, 28.48, 1.693956482),
    4: Table2A(4, "Mg2+", 0.5, 0.12, 28.48, 1.693956482),
    5: Table2A(5, "Cl−", 0.5, 0.12, 28.48, 1.693956482),
    6: Table2A(6, "HCO3−", 0.5, 0.12, 28.48, 1.693956482),
    7: Table2A(7, "PO4−", 0.5, 0.12, 28.48, 1.693956482),
    8: Table2A(8, "SO4−", 0.5, 0.12, 28.48, 1.693956482),
    9: Table2A(9, "NO3−", 0.5, 0.12, 28.48, 1.693956482),
    10: Table2A(10, "NH4+", 0.5, 0.12, 28.48, 1.693956482),
    11: Table2A(11, "Fe2+", 0.5, 0.12, 28.48, 1.693956482),
    12: Table2A(12, "Fe3+", 0.5, 0.12, 28.48, 1.693956482),
    13: Table2A(13, "Zn2+", 0.5, 0.12, 28.48, 1.693956482),
    14: Table2A(14, "Cu2+", 0.5, 0.12, 28.48, 1.693956482),
    15: Table2A(15, "Mn2+", 0.5, 0.12, 28.48, 1.693956482),
    16: Table2A(16, "Pb2+", 0.5, 0.12, 28.48, 1.693956482),
    17: Table2A(17, "Hg2+", 0.5, 0.12, 28.48, 1.693956482),
    18: Table2A(18, "Cd2+", 0.5, 0.12, 28.48, 1.693956482),
    19: Table2A(19, "Al3+", 0.5, 0.12, 28.48, 1.693956482),
    20: Table2A(20, "Cr3+", 0.5, 0.12, 28.48, 1.693956482),
    21: Table2A(21, "Co2+", 0.5, 0.12, 28.48, 1.693956482),
    22: Table2A(22, "Ni2+", 0.5, 0.12, 28.48, 1.693956482),
    23: Table2A(23, "Ag+", 0.5, 0.12, 28.48, 1.693956482),
    24: Table2A(24, "Ba2+", 0.5, 0.12, 28.48, 1.693956482),
    25: Table2A(25, "Sr2+", 0.5, 0.12, 28.48, 1.693956482),

    # Troponin samples
    26: Table2A(26, "Troponin T", None, None, 28.48, 1.693956482),
    27: Table2A(27, "Troponin I", None, None, 28.48, 1.693956482),
    28: Table2A(28, "Troponin C", None, None, 28.48, 1.693956482),
}


# -----------------------------
# TABLE 2B — OUTPUT PARAMETERS
# -----------------------------
TABLE_2B: Dict[int, Table2B] = {
    1: Table2B(1, 2e-8, 2.15e-13, 1.82e-5, 1.693956840),
    2: Table2B(2, 3e-8, 2.20e-13, 1.82e-5, 1.693956900),
    3: Table2B(3, 4e-8, 2.25e-13, 1.82e-5, 1.693956950),
    # ... continue filling for IDs 4–28 ...
}


def analyze_device_v2(id: int) -> Dict[str, Any]:
    if id not in TABLE_2A or id not in TABLE_2B:
        raise ValueError(f"ID {id} not found in Patent 2 tables.")

    a = TABLE_2A[id]
    b = TABLE_2B[id]

    delta_f = b.f2_mhz - a.f1_mhz
    am_computed = (b.af_mhz / b.f2_mhz) * b.m_g

    return {
        "id": id,
        "ion": a.ion,
        "mass_g": a.mass_g,
        "concentration_m": a.concentration_m,
        "dilution_volume_ml": a.dilution_volume_ml,
        "frequency_f1_mhz": a.f1_mhz,
        "frequency_f2_mhz": b.f2_mhz,
        "delta_f_mhz": delta_f,
        "af_mhz": b.af_mhz,
        "m_g": b.m_g,
        "am_table": b.am_table,
        "am_computed": am_computed,
    }
