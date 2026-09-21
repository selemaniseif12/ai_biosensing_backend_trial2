# app/routers/profile_router.py

import os
import base64
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response

router = APIRouter()

# Store profile image inside /app/profile.png
PROFILE_PATH = os.path.join("app", "profile.png")


@router.get("/profile/image")
def get_profile_image():
    """
    Returns the profile image as raw Base64 text.
    Frontend expects plain text, not JSON.
    """
    if not os.path.exists(PROFILE_PATH):
        raise HTTPException(status_code=404, detail="Profile image not found")

    with open(PROFILE_PATH, "rb") as f:
        base64_data = base64.b64encode(f.read()).decode("utf-8")

    # IMPORTANT: return raw Base64 text
    return Response(content=base64_data, media_type="text/plain")


@router.post("/profile/image")
async def upload_profile_image(file: UploadFile = File(...)):
    """
    Uploads a new profile image and replaces the existing one.
    """
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Only PNG or JPEG images are allowed")

    contents = await file.read()
    with open(PROFILE_PATH, "wb") as f:
        f.write(contents)

    return {"message": "Profile image updated successfully"}
