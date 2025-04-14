# backend/app/core/config.py
from pydantic_settings import BaseSettings  # <-- Cambio aquí

class Settings(BaseSettings):
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()