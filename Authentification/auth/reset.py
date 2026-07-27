import secrets
from datetime import datetime, timedelta, timezone

def generate_reset_token() -> tuple[str, str]:
    """Generate a secure password reset token and its expiration time. Returns (token, expiry_string)."""
    token = secrets.toke_urlsafe(32)
    expiry = (datetime.now(timezone.utc) + timedelta(minutes=30)).isoformat()
    return token, expiry

def verify_reset_token(stored_token: str, stored_expiry: str, submitted_token: str) -> bool:
    """ Verify submitted token matches stored token and hasn't expired."""
    if stored_token != submitted_token:
        return False
    expiry = datetime.fromisoformat(stored_expiry)
    if datetime.now(timezone.utc) > expiry:
        return False
    return True


