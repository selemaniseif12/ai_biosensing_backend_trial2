import secrets

def generate_api_key() -> str:
    # Generates a secure 64-character hex API key
    return secrets.token_hex(32)
