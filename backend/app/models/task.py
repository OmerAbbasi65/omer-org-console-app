"""
Task Model - SQLModel Schema for Level 1 (Core Features)

As defined in: specs/002-todo-web-app-level1/contracts/data-model.md
"""

from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator


class Task(SQLModel, table=True):
    """
    Task entity for Level 1 (Core) features.

    Represents a single todo item with basic CRUD capabilities.
    """

    __tablename__ = "tasks"

    # Primary Key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        description="Unique identifier (UUID v4)"
    )

    # Core Fields (Level 1)
    title: str = Field(
        max_length=200,
        min_length=1,
        nullable=False,
        description="Task title (required, 1-200 characters)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        nullable=True,
        description="Optional task description (max 1000 characters)"
    )

    completed: bool = Field(
        default=False,
        nullable=False,
        description="Completion status (defaults to false)"
    )

    # Timestamps (auto-managed)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Creation timestamp (UTC, ISO-8601)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last update timestamp (UTC, ISO-8601)"
    )

    # Level 2 fields (deferred, nullable for schema evolution)
    # priority: Optional[str] = Field(default=None, max_length=10)
    # tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

    # Level 3 fields (deferred, nullable for schema evolution)
    # due_date: Optional[datetime] = Field(default=None)
    # recurrence: Optional[str] = Field(default=None, max_length=20)
    # reminder_time: Optional[datetime] = Field(default=None)

    class Config:
        """Pydantic configuration"""
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2026-01-08T10:30:00.000Z",
                "updated_at": "2026-01-08T10:30:00.000Z"
            }
        }


class TaskCreate(BaseModel):
    """Schema for creating a new task"""

    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title (required)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional task description"
    )

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Task title cannot be empty or whitespace only')
        return v.strip()

    class Config:
        schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread"
            }
        }


class TaskUpdate(BaseModel):
    """Schema for updating a task (partial updates allowed)"""

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Updated task title"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Updated task description"
    )

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Task title cannot be empty or whitespace only')
        return v.strip() if v else v

    class Config:
        schema_extra = {
            "example": {
                "title": "Buy groceries and fruits"
            }
        }


class TaskResponse(BaseModel):
    """Schema for task responses (read operations)"""

    id: UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Allow reading from ORM models
        from_attributes = True  # Pydantic v2
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2026-01-08T10:30:00.000Z",
                "updated_at": "2026-01-08T10:30:00.000Z"
            }
        }


class TaskList(BaseModel):
    """Schema for list responses"""

    tasks: List[TaskResponse]
    total: int

    class Config:
        schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Buy groceries",
                        "description": "Milk, eggs, bread",
                        "completed": False,
                        "created_at": "2026-01-08T10:30:00.000Z",
                        "updated_at": "2026-01-08T10:30:00.000Z"
                    }
                ],
                "total": 1
            }
        }
