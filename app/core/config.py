# backend/app/core/config.py
from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str
    class Config:
        env_file = ".env"

settings = Settings()