from fastapi import APIRouter
import csv
import os

router = APIRouter(prefix="/app")

CSV_PATH = os.path.join("data", "profile_image.csv")

@router.get("/profile/image")
def get_profile_image():
    with open(CSV_PATH, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        row = next(reader)
        return {"image": row[0]}
