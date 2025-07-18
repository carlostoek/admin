# models.py
# Modelos de datos para usuarios y tokens

from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    telegram_id: int
    username: str
    role: str
    vip_expiry: Optional[int]
    created_at: int

@dataclass
class Token:
    token: str
    name: str
    price: int
    duration: int
    created_by: int
    created_at: int
    used_by: Optional[int]
    used_at: Optional[int]