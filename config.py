import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_URL: str
    # Add more environment-specific settings here

    class Config:
        env_file = ".env"  # Load environment variables from `.env` file

settings = Settings()
