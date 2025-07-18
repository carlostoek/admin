# config.py
import os
from dotenv import load_dotenv
from pydantic import BaseSettings, validator

load_dotenv()

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: str
    VIP_CHANNEL_ID: str
    FREE_CHANNEL_ID: str
    DATABASE_URL: str = "data.db"
    FREE_CHANNEL_RULES_URL: str = ""
    FREE_CHANNEL_DELAY: int = 5  # minutos
    
    @validator('VIP_CHANNEL_ID', 'FREE_CHANNEL_ID', pre=True)
    def validate_channel_ids(cls, v):
        if not v.startswith('-100'):
            raise ValueError("ID de canal debe empezar con -100")
        return v
    
    @validator('ADMIN_IDS')
    def validate_admin_ids(cls, v):
        if not all(id.strip().isdigit() for id in v.split(',')):
            raise ValueError("ADMIN_IDS debe contener solo números separados por comas")
        return v

    class Config:
        env_file = ".env"

settings = Settings()
