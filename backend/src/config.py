"""Configuration module loading environment variables."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "postgresql://localhost/todo_db"

    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    backend_reload: bool = True

    # CORS
    allowed_origins: str = "http://localhost:3000"

    # Logging
    log_level: str = "INFO"

    # API
    api_v1_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


settings = Settings()
