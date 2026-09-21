from fastapi import APIRouter
import os
import base64

router = APIRouter(prefix="/app")

# Absolute path to the directory where THIS file lives
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Absolute path to the project root (one level up)
ROOT_DIR = os.path.dirname(CURRENT_DIR)

# Absolute path to the data folder
DATA_DIR = os.path.join(ROOT_DIR, "data")

# Absolute path to the CSV file
CSV_PATH = os.path.join(DATA_DIR, "profile_image.csv")

@router.get("/profile/image")
def get_profile_image():
    # Read filename from CSV
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
        filename = lines[1].strip()  # second line: profile.png

    image_path = os.path.join(DATA_DIR, filename)

    # Read and encode the real image file
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")

    return {"image": f"data:image/png;base64,{encoded}"}

