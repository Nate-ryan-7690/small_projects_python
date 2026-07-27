import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "this-is-a-32-byte-secret-key-ok!"  # In production, use a secure method to store this key

def generate_token(user_id: str, username: str, role: str) -> str:
    """Generate a JWT token for a user."""
    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)  # Token expires in 1 hour
    }

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> dict | None:
    """Verify a JWT token and return the payload if valid"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None # Token is invalid


