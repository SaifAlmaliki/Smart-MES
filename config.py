"""
Configuration settings for the FastAPI application.
"""

from pydantic import BaseSettings

class Settings(BaseSettings):
    """Base settings for the application."""
    PROJECT_NAME: str = "Manufacturing Execution System"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/mes"

    class Config:
        """Pydantic configuration."""
        env_file = ".env"

settings = Settings()
