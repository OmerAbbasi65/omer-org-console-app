"""
Application Configuration
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database
    DATABASE_URL: str

    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Todo API"

    # CORS
    FRONTEND_URL: str = "http://localhost:3000"

    # Environment
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
