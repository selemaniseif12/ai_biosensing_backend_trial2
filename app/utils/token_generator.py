import secrets
import string


def generate_token(length: int = 32) -> str:
    """
    Generates a secure, URL‑safe token for service access.
    Uses Python's secrets module for cryptographic randomness.
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
