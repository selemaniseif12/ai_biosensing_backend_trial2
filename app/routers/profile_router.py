# app/routers/profile_router.py

import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

PROFILE_PATH = os.path.join("app", "profile.png")


@router.get("/profile/image")
def get_profile_image():
    """
    Returns the current profile image.
    """
    if not os.path.exists(PROFILE_PATH):
        raise HTTPException(status_code=404, detail="Profile image not found")

    return FileResponse(PROFILE_PATH, media_type="image/png")


@router.post("/profile/image")
async def upload_profile_image(file: UploadFile = File(...)):
    """
    Uploads a new profile image and replaces the existing one.
    """
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Only PNG or JPEG images are allowed")

    # Save uploaded file as profile.png
    contents = await file.read()
    with open(PROFILE_PATH, "wb") as f:
        f.write(contents)

    return {"message": "Profile image updated successfully"}
