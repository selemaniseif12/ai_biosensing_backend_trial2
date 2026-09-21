# app/services/analyzer_v5_service.py

import logging
from functools import lru_cache
from math import ceil
from pathlib import Path
from typing import Dict, Any

import pandas as pd

logger = logging.getLogger("analyzers")

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "ml" / "data"

DEVICE_FILES = {
    1: "Device 1.csv",
    2: "Device2.csv",
    3: "Device3.csv",
    4: "Device4.csv",
    5: "Device5.csv",
}

ANTIGEN_TABLE_FILE = "Table 1 Antigen Antibody.csv"


# ---------------------------------------------------------
# LOAD ANTIGEN TABLE (CACHED)
# ---------------------------------------------------------
@lru_cache(maxsize=1)
def _load_antigen_table() -> pd.DataFrame:
    logger.info("[Analyzer v5] Loading antigen table")

    try:
        path = DATA_PATH / ANTIGEN_TABLE_FILE
        df = pd.read_csv(path)
        df = df.rename(columns={"Mass (fg)": "virus_mass_fg"})
        logger.info("[Analyzer v5] Antigen table loaded successfully")
        return df

    except Exception as e:
        logger.error(f"[Analyzer v5] ERROR loading antigen table: {str(e)}")
        raise


# ---------------------------------------------------------
# LOAD DEVICE TABLE (CACHED PER DEVICE)
# ---------------------------------------------------------
@lru_cache(maxsize=None)
def _load_device_table(device_id: int) -> pd.DataFrame:
    logger.info(f"[Analyzer v5] Loading device table for device_id={device_id}")

    try:
        if device_id not in DEVICE_FILES:
            raise ValueError(f"Unsupported device_id: {device_id}")

        path = DATA_PATH / DEVICE_FILES[device_id]
        df = pd.read_csv(path)
        df = df.rename(columns={
            "f (MHz)": "f_MHz",
            "∆f (MHz)": "delta_f_MHz",
            "∆m (g)": "delta_m_g",
            "Mass (g)": "device_mass_g",
        })
        df["device_id"] = device_id

        logger.info(f"[Analyzer v5] Device table loaded successfully for device_id={device_id}")
        return df

    except Exception as e:
        logger.error(f"[Analyzer v5] ERROR loading device table for device_id={device_id}: {str(e)}")
        raise


# ---------------------------------------------------------
# MAIN ANALYZER V5
# ---------------------------------------------------------
def run_analyzer_v5(device_id: int, virus_id: int) -> Dict[str, Any]:
    logger.info(f"[Analyzer v5] run_analyzer_v5 called with device_id={device_id}, virus_id={virus_id}")

    try:
        antigen_df = _load_antigen_table()
        device_df = _load_device_table(device_id)

        # Lookup virus in antigen table
        virus_row = antigen_df[antigen_df["ID"] == virus_id]
        if virus_row.empty:
            logger.error(f"[Analyzer v5] Virus ID {virus_id} not found in antigen table")
            raise ValueError(f"Virus ID {virus_id} not found in antigen table.")

        # Lookup virus in device table
        device_row = device_df[device_df["ID"] == virus_id]
        if device_row.empty:
            logger.error(f"[Analyzer v5] Virus ID {virus_id} not found in device {device_id} table")
            raise ValueError(f"Virus ID {virus_id} not found in device {device_id} table.")

        virus_row = virus_row.iloc[0]
        device_row = device_row.iloc[0]

        virus_mass_fg = float(virus_row["virus_mass_fg"])
        virus_mass_g = virus_mass_fg * 1e-15

        device_mass_resolution_g = float(device_row["delta_m_g"])
        delta_f_MHz = float(device_row["delta_f_MHz"])
        f_MHz = float(device_row["f_MHz"])

        if virus_mass_g <= 0:
            logger.error("[Analyzer v5] Virus mass must be positive")
            raise ValueError("Virus mass must be positive.")

        required_count = ceil(device_mass_resolution_g / virus_mass_g)
        binding_profile = f"{virus_row['Antibody']} | {virus_row['Antigen']}"

        result = {
            "device_id": device_id,
            "virus_id": virus_id,
            "virus": virus_row["Virus"],
            "virus_mass_fg": virus_mass_fg,
            "device_mass_resolution_g": device_mass_resolution_g,
            "required_virus_count": required_count,
            "f_MHz": f_MHz,
            "delta_f_MHz": delta_f_MHz,
            "binding_profile": binding_profile,
        }

        logger.info(f"[Analyzer v5] Analysis result: {result}")
        return result

    except Exception as e:
        logger.error(f"[Analyzer v5] ERROR in run_analyzer_v5: {str(e)}")
        raise
