import secrets
from datetime import datetime, timedelta

def generate_token(length: int = 32) -> str:
    return secrets.token_urlsafe(length)

def get_token_expiry(hours: int = 24) -> datetime:
    return datetime.utcnow() + timedelta(hours=hours)