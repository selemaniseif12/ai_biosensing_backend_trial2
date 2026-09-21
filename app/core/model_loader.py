# app/core/model_loader.py

import os
import pathlib
import requests
import joblib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

V2_LOCAL_PATH = BASE_DIR / "models" / "sim_model_v2_100.pkl"
V6_LOCAL_PATH = BASE_DIR / "models" / "sim_model_v6_100.pkl"


# ---------------------------------------------------------
# ROBUST HUGGINGFACE DOWNLOADER
# ---------------------------------------------------------
def _download_model(url: str, local_path: pathlib.Path) -> None:
    local_path.parent.mkdir(parents=True, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*"
    }

    with requests.get(
        url,
        headers=headers,
        stream=True,
        allow_redirects=True,
        timeout=120
    ) as r:
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


# ---------------------------------------------------------
# SAFE LOCAL LOADER (DELETES CORRUPT FILES)
# ---------------------------------------------------------
def _load_model(local_path: pathlib.Path):
    try:
        return joblib.load(local_path)
    except Exception:
        # Corrupted file (like KeyError 118) → delete and force re-download
        if local_path.exists():
            local_path.unlink()
        raise


# ---------------------------------------------------------
# FALLBACK LOADER (LOCAL → HUGGINGFACE → ERROR)
# ---------------------------------------------------------
def load_model_with_fallback(url_env_name: str, local_path: pathlib.Path):
    """
    1. Try local file.
    2. If missing or corrupted and URL exists → download from HuggingFace, then load.
    3. If no URL or download fails → raise clean error.
    """
    url = os.getenv(url_env_name)

    # 1. Try local cached file
    if local_path.exists():
        try:
            return _load_model(local_path)
        except Exception:
            # Corrupt local file already deleted in _load_model; fall through to download
            pass

    # 2. No URL → cannot download
    if not url:
        raise RuntimeError(
            f"{url_env_name} not set and local model not found at {local_path}"
        )

    # 3. Download from HuggingFace and load
    try:
        _download_model(url, local_path)
        return _load_model(local_path)
    except Exception as e:
        raise RuntimeError(
            f"Failed to download/load model from {url} → {e}"
        )
