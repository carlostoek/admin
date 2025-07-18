# utils/security.py
# Protección básica contra ataques comunes

def sanitize_text(text):
    """Sanitiza texto para evitar inyecciones."""
    return text.replace("<", "&lt;").replace(">", "&gt;")