from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./smartrecruit.db" # Using SQLite for easy local testing
    # For Postgres: "postgresql://user:pass@localhost:5432/smartrecruit"
    
    APP_NAME: str = "SmartRecruit AI"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()