import hashlib
import os
import secrets

def get_password_hash(password: str) -> str:
    """Generates a secure PBKDF2-HMAC-SHA256 password hash with salt."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"pbkdf2:sha256:100000${salt}${key.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a stored PBKDF2 hash string."""
    try:
        if not hashed_password.startswith("pbkdf2:sha256:"):
            # Fallback for old dev placeholder hashes
            return hashed_password == f"hashed_{plain_password}" or hashed_password == plain_password

        parts = hashed_password.split("$")
        if len(parts) != 3:
            return False

        _, salt, expected_hex = parts
        key = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return secrets.compare_digest(key.hex(), expected_hex)
    except Exception:
        return False
