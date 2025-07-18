# tests/test_tokens.py
# Test unitario para generación de tokens

from utils.tokens import generate_token

def test_generate_token_length():
    token = generate_token()
    assert len(token) >= 16