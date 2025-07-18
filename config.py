# config.py
# Configuración y carga de variables de entorno

import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: str  # Coma separados
    VIP_CHANNEL_ID: int
    FREE_CHANNEL_ID: int
    DATABASE_URL: str
    PAYMENT_PROVIDER_TOKEN: str
    METRICS_PORT: int = 8001

    class Config:
        env_file = ".env"

settings = Settings()