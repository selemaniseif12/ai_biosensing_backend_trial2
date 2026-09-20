from fastapi import APIRouter
import base64
import os

router = APIRouter(prefix="/app")

PROFILE_IMAGE_PATH = os.path.join("data", "profile.png")

@router.get("/profile/image")
def get_profile_image():
    with open(PROFILE_IMAGE_PATH, "rb") as img:
        encoded = base64.b64encode(img.read()).decode("utf-8")
    return encoded  # RAW BASE64 TEXT ONLY
