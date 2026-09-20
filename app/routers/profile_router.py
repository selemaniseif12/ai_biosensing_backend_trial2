from fastapi import APIRouter
import base64
import os

router = APIRouter(prefix="/app")

PROFILE_JSON_PATH = os.path.join("data", "profile.json")
PROFILE_IMAGE_PATH = os.path.join("data", "profile.png")

@router.get("/profile")
def get_profile():
    # Load JSON profile data
    with open(PROFILE_JSON_PATH, "r", encoding="utf-8") as f:
        profile = f.read()

    # Load image and convert to Base64
    with open(PROFILE_IMAGE_PATH, "rb") as img:
        encoded_image = base64.b64encode(img.read()).decode("utf-8")

    return {
        "profile": profile,
        "image": encoded_image
    }
