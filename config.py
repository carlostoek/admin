from pydantic_settings import BaseSettings
from pydantic import Field, validator
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    BOT_TOKEN: str = Field(..., env="BOT_TOKEN")
    ADMIN_IDS: str = Field(..., env="ADMIN_IDS")
    VIP_CHANNEL_ID: int = Field(..., env="VIP_CHANNEL_ID")
    FREE_CHANNEL_ID: int = Field(..., env="FREE_CHANNEL_ID")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    PAYMENT_PROVIDER_TOKEN: str = Field(..., env="PAYMENT_PROVIDER_TOKEN")
    METRICS_PORT: int = Field(8001, env="METRICS_PORT")

    @validator("FREE_CHANNEL_ID", "VIP_CHANNEL_ID", pre=True)
    def remove_whitespace(cls, v):
        if isinstance(v, str):
            return int(v.strip())  # Elimina espacios y convierte a int
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
