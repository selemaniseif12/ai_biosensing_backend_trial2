from fastapi import Header, HTTPException
from .firebase_admin import verify_firebase_token

async def firebase_auth(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.split(" ")[1]
    decoded = verify_firebase_token(token)

    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")

    return decoded
