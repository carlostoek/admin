from pydantic_settings import BaseSettings
from pydantic import Field
import os
from dotenv import load_dotenv

# Cargar .env (opcional, solo como respaldo)
load_dotenv()

class Settings(BaseSettings):
    BOT_TOKEN: str = Field(..., env="BOT_TOKEN")
    ADMIN_IDS: str = Field(..., env="ADMIN_IDS")  # Coma separados
    VIP_CHANNEL_ID: int = Field(..., env="VIP_CHANNEL_ID")
    FREE_CHANNEL_ID: int = Field(..., env="FREE_CHANNEL_ID")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    PAYMENT_PROVIDER_TOKEN: str = Field(..., env="PAYMENT_PROVIDER_TOKEN")
    METRICS_PORT: int = Field(8001, env="METRICS_PORT")

    class Config:
        # Prioriza variables de entorno sobre .env
        env_file = ".env"  # Respaldo
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignora variables no definidas

settings = Settings()
