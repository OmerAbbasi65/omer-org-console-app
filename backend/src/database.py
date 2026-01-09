"""Database connection and session management."""

from sqlmodel import Session, create_engine
from sqlalchemy.pool import NullPool
import os
from typing import Generator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

engine = create_engine(
    DATABASE_URL,
    echo=True if os.getenv("LOG_LEVEL") == "DEBUG" else False,
    poolclass=NullPool if "neon.tech" in DATABASE_URL else None,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)


def get_session() -> Generator[Session, None, None]:
    """Dependency for FastAPI routes to get database session."""
    with Session(engine) as session:
        yield session


def init_db() -> None:
    """Initialize database - create all tables."""
    from sqlmodel import SQLModel
    from src.models.task import Task  # noqa: F401

    SQLModel.metadata.create_all(engine)
