import os
import firebase_admin
from firebase_admin import credentials, auth

# Get absolute path to this folder (app/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build full path to your Firebase key file
KEY_PATH = os.path.join(BASE_DIR, "backend_serviceAccountKey.json")

cred = credentials.Certificate(KEY_PATH)
firebase_admin.initialize_app(cred)


def verify_firebase_token(token: str):
    try:
        decoded = auth.verify_id_token(token)
        return decoded
    except Exception:
        return None
