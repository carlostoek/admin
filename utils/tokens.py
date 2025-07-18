# utils/tokens.py
# Generación segura de tokens únicos

import secrets

def generate_token(length=16):
    """Genera un token seguro y único para acceso VIP."""
    return secrets.token_urlsafe(length)