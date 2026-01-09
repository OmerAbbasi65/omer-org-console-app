# Data Model: Task Entity (SQLModel Schema)

**Phase**: Phase 2 - Level 1 (Core Features)
**ORM**: SQLModel (SQLAlchemy + Pydantic)
**Database**: Neon PostgreSQL
**Date**: 2026-01-08

## Overview

This document defines the Task entity schema using SQLModel, which serves as both:
1. **Database ORM** (SQLAlchemy table definition)
2. **API Validation** (Pydantic model for FastAPI)

SQLModel provides type safety, automatic validation, and seamless database-to-API integration.

---

## Task Entity - Level 1 Schema

### SQLModel Definition

```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

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
        sa_column_kwargs={"onupdate": datetime.utcnow},
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
```

---

## Field Specifications

### Level 1 Fields (Implemented)

| Field | Type | Constraints | Default | Nullable | Description |
|-------|------|-------------|---------|----------|-------------|
| `id` | UUID | Primary Key, Indexed | auto-generated | No | Unique task identifier (UUID v4) |
| `title` | string | 1-200 chars, non-empty | - | No | Task title (required) |
| `description` | string | max 1000 chars | `null` | Yes | Optional task description |
| `completed` | boolean | - | `false` | No | Completion status |
| `created_at` | datetime | ISO-8601, UTC | `now()` | No | Creation timestamp (immutable) |
| `updated_at` | datetime | ISO-8601, UTC | `now()` | No | Last update timestamp (auto-updated) |

### Level 2 Fields (Deferred)

| Field | Type | Constraints | Default | Nullable | Description |
|-------|------|-------------|---------|----------|-------------|
| `priority` | enum | "high", "medium", "low" | `null` | Yes | Task priority level |
| `tags` | array[string] | - | `[]` | Yes | Task categorization tags |

### Level 3 Fields (Deferred)

| Field | Type | Constraints | Default | Nullable | Description |
|-------|------|-------------|---------|----------|-------------|
| `due_date` | datetime | ISO-8601, UTC | `null` | Yes | Task deadline |
| `recurrence` | enum | "none", "daily", "weekly", "monthly" | `"none"` | Yes | Recurrence pattern |
| `reminder_time` | datetime | ISO-8601, UTC | `null` | Yes | Reminder trigger time |

---

## Database Schema (PostgreSQL)

### Table: `tasks`

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL CHECK (length(trim(title)) > 0),
    description VARCHAR(1000) DEFAULT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Level 2 (deferred)
    -- priority VARCHAR(10) DEFAULT NULL,
    -- tags JSONB DEFAULT NULL,

    -- Level 3 (deferred)
    -- due_date TIMESTAMP DEFAULT NULL,
    -- recurrence VARCHAR(20) DEFAULT NULL,
    -- reminder_time TIMESTAMP DEFAULT NULL
);

-- Indexes for Level 1
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
CREATE INDEX idx_tasks_completed ON tasks(completed);

-- Indexes for Level 2 (deferred)
-- CREATE INDEX idx_tasks_priority ON tasks(priority);
-- CREATE INDEX idx_tasks_tags ON tasks USING GIN(tags);

-- Indexes for Level 3 (deferred)
-- CREATE INDEX idx_tasks_due_date ON tasks(due_date);

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## Pydantic Schemas for API

SQLModel allows creating specialized schemas for different API operations:

### TaskCreate (POST /api/v1/tasks)

```python
from pydantic import BaseModel, Field, validator

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
```

### TaskUpdate (PATCH /api/v1/tasks/{id})

```python
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
```

### TaskResponse (All GET responses)

```python
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
```

### TaskList (GET /api/v1/tasks)

```python
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
```

---

## Validation Rules

### Title Validation
1. **Required**: Cannot be `null` or missing
2. **Non-empty**: Must contain at least 1 non-whitespace character
3. **Max Length**: 200 characters (after trimming)
4. **Trimming**: Leading/trailing whitespace is automatically removed

### Description Validation
1. **Optional**: Can be `null` or omitted
2. **Max Length**: 1000 characters (if provided)
3. **Nullable**: Can be set to `null` to clear existing description

### ID Validation
1. **Format**: Must be valid UUID v4
2. **Uniqueness**: Enforced by database primary key constraint
3. **Immutable**: Cannot be changed after creation

### Timestamp Validation
1. **Format**: ISO-8601 datetime string
2. **Timezone**: Stored and returned in UTC
3. **Immutability**: `created_at` never changes; `updated_at` auto-updates

---

## Database Migration Strategy

### Initial Migration (Level 1)

Using Alembic (SQLAlchemy migration tool):

```python
# alembic/versions/001_initial_schema.py
"""Initial schema - Level 1 Core features

Revision ID: 001
Revises:
Create Date: 2026-01-08

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.String(1000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    # Indexes
    op.create_index('idx_tasks_created_at', 'tasks', ['created_at'], unique=False)
    op.create_index('idx_tasks_completed', 'tasks', ['completed'], unique=False)

    # Trigger for updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER update_tasks_updated_at
            BEFORE UPDATE ON tasks
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
    """)

def downgrade():
    op.drop_table('tasks')
```

### Future Migrations (Level 2 & 3)

Migrations will ADD columns (never remove or rename) to maintain backward compatibility:

```python
# Level 2 migration (example)
def upgrade():
    op.add_column('tasks', sa.Column('priority', sa.String(10), nullable=True))
    op.add_column('tasks', sa.Column('tags', postgresql.JSONB(), nullable=True))
    op.create_index('idx_tasks_priority', 'tasks', ['priority'])
    op.create_index('idx_tasks_tags', 'tasks', ['tags'], postgresql_using='gin')
```

---

## Schema Evolution Principles

1. **Additive Only**: New fields are always nullable (no breaking changes)
2. **No Renames**: Never rename columns (add new, deprecate old)
3. **No Deletions**: Never drop columns (mark as deprecated)
4. **Default Values**: New fields have sensible defaults
5. **Backward Compatibility**: Level 1 apps work with Level 2+ schema

---

## Data Integrity Constraints

### Database-Level Constraints
- `id` PRIMARY KEY (uniqueness enforced)
- `title` NOT NULL (required field)
- `completed` NOT NULL (boolean, never null)
- `created_at` NOT NULL (always set)
- `updated_at` NOT NULL (always set)

### Application-Level Validation (Pydantic)
- Title length: 1-200 characters
- Description length: max 1000 characters
- Title trimming: whitespace removed
- Empty title rejection: whitespace-only titles rejected

---

## Performance Considerations

### Indexes (Level 1)
- `PRIMARY KEY (id)`: Automatic unique index
- `idx_tasks_created_at`: For sorting by creation time
- `idx_tasks_completed`: For filtering completed/incomplete tasks

### Query Optimization
- Use `SELECT *` sparingly (specify needed columns)
- Pagination recommended for large datasets (Level 2+)
- Connection pooling for concurrent requests

### Neon-Specific Optimizations
- Auto-suspend after inactivity (cost savings)
- Auto-scaling for traffic spikes
- Instant database branching for testing

---

## Testing Data

### Seed Data for Development

```python
from datetime import datetime, timedelta
from uuid import uuid4

seed_tasks = [
    {
        "id": uuid4(),
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": uuid4(),
        "title": "Finish project report",
        "description": None,
        "completed": True,
        "created_at": datetime.utcnow() - timedelta(hours=2),
        "updated_at": datetime.utcnow() - timedelta(minutes=30)
    },
    {
        "id": uuid4(),
        "title": "Call dentist for appointment",
        "description": "Check availability for next week",
        "completed": False,
        "created_at": datetime.utcnow() - timedelta(days=1),
        "updated_at": datetime.utcnow() - timedelta(days=1)
    }
]
```

---

## Constitutional Compliance

This data model follows the Phase 2 constitution:

✅ **SQLModel as Canonical Schema**: Single source of truth
✅ **Neon PostgreSQL**: Serverless, persistent storage
✅ **Schema Evolution**: Nullable future fields for Level 2/3
✅ **Timezone-Aware**: All timestamps in UTC
✅ **Globally Unique IDs**: UUID v4 for all tasks
✅ **No Breaking Changes**: Additive-only schema evolution
