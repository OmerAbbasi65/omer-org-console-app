"""
Database Connection and Session Management

Handles SQLModel engine creation and session lifecycle.
"""

from sqlmodel import SQLModel, Session, create_engine
from app.config import settings
from typing import Generator


# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True if settings.ENVIRONMENT == "development" else False,
    pool_pre_ping=True,  # Test connections before using
)


def create_db_and_tables():
    """
    Create all database tables.

    Should be called on application startup.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI routes to get a database session.

    Usage:
        @app.get("/tasks")
        def get_tasks(session: Session = Depends(get_session)):
            ...

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session
