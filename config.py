import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MES System"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/mes-operations"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # JWT expiration in minutes
    # Add more environment-specific settings here

    class Config:
        env_file = ".env"  # Load environment variables from `.env` file

settings = Settings()
