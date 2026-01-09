"""Task models for database and API."""

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from pydantic import field_validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4


class Task(SQLModel, table=True):
    """Task database model."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium", max_length=10)
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    due_date: Optional[datetime] = Field(default=None)
    recurrence: str = Field(default="none", max_length=20)
    parent_id: Optional[UUID] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(SQLModel):
    """Model for creating a task."""

    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    priority: Optional[str] = Field(default="medium")
    tags: Optional[List[str]] = Field(default_factory=list)
    due_date: Optional[datetime] = None
    recurrence: Optional[str] = Field(default="none")

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v):
        if v not in ["low", "medium", "high"]:
            raise ValueError("Priority must be low, medium, or high")
        return v

    @field_validator("recurrence")
    @classmethod
    def validate_recurrence(cls, v):
        if v not in ["none", "daily", "weekly", "monthly"]:
            raise ValueError("Recurrence must be none, daily, weekly, or monthly")
        return v


class TaskUpdate(SQLModel):
    """Model for updating a task (all fields optional)."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    recurrence: Optional[str] = None

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v):
        if v is not None and v not in ["low", "medium", "high"]:
            raise ValueError("Priority must be low, medium, or high")
        return v

    @field_validator("recurrence")
    @classmethod
    def validate_recurrence(cls, v):
        if v is not None and v not in ["none", "daily", "weekly", "monthly"]:
            raise ValueError("Recurrence must be none, daily, weekly, or monthly")
        return v


class TaskResponse(SQLModel):
    """Model for API responses."""

    id: UUID
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    tags: List[str]
    due_date: Optional[datetime]
    recurrence: str
    parent_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
