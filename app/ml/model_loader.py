# app/ml/model_loader.py

import os
import pickle
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CACHE_DIR = Path("model_cache")
CACHE_DIR.mkdir(exist_ok=True)

def load_hf_model(filename: str):
    local_path = CACHE_DIR / filename
    if not local_path.exists():
        raise RuntimeError(
            f"Model file not found: {local_path}\n"
            f"Download RAW .pkl from HuggingFace and place it in model_cache/"
        )
    with open(local_path, "rb") as f:
        return pickle.load(f)

virus_classifier = load_hf_model("sim_model_v2_100.pkl")
