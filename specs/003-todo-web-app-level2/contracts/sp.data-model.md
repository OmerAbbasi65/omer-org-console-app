# Data Model: Level 2 (Organization) Extensions

**Phase**: Phase 2 - Level 2 (Organization Features)
**ORM**: SQLModel (SQLAlchemy + Pydantic)
**Database**: Neon PostgreSQL
**Date**: 2026-01-09

## Overview

This document defines database schema extensions for Level 2 (Organization) features. All changes are **additive only** and maintain full backward compatibility with Level 1.

---

## Task Entity - Level 2 Schema Extensions

### SQLModel Definition (Complete with Level 2)

```python
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator

class Task(SQLModel, table=True):
    """
    Task entity with Level 1 (Core) and Level 2 (Organization) features.
    """

    __tablename__ = "tasks"

    # Primary Key (Level 1)
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

    # Organization Fields (Level 2 - NEW)
    priority: Optional[str] = Field(
        default=None,
        max_length=10,
        nullable=True,
        description="Task priority: high, medium, low, or null"
    )

    tags: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON),
        nullable=False,
        description="Task tags (empty array by default)"
    )

    # Timestamps (Level 1)
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

    # Level 3 fields (deferred, nullable for schema evolution)
    # due_date: Optional[datetime] = Field(default=None)
    # recurrence: Optional[str] = Field(default=None, max_length=20)
    # reminder_time: Optional[datetime] = Field(default=None)

    @validator('priority')
    def validate_priority(cls, v):
        """Validate priority enum values"""
        if v is not None and v not in ['high', 'medium', 'low']:
            raise ValueError('Priority must be high, medium, low, or null')
        return v

    @validator('tags')
    def validate_tags(cls, v):
        """Validate tags array constraints"""
        if v is None:
            return []
        if len(v) > 20:
            raise ValueError('Maximum 20 tags allowed')
        for tag in v:
            if len(tag) > 50:
                raise ValueError(f'Tag "{tag}" exceeds 50 character limit')
            if not tag.strip():
                raise ValueError('Tags cannot be empty or whitespace only')
        # Deduplicate (preserve order, case-sensitive)
        seen = set()
        deduped = []
        for tag in v:
            tag_stripped = tag.strip()
            if tag_stripped not in seen:
                seen.add(tag_stripped)
                deduped.append(tag_stripped)
        return deduped

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Deploy application",
                "description": "Deploy to staging environment",
                "completed": false,
                "priority": "high",
                "tags": ["work", "urgent", "deployment"],
                "created_at": "2026-01-09T10:30:00.000Z",
                "updated_at": "2026-01-09T10:30:00.000Z"
            }
        }
```

---

## Field Specifications

### Level 2 Fields (NEW)

| Field | Type | Constraints | Default | Nullable | Index | Description |
|-------|------|-------------|---------|----------|-------|-------------|
| `priority` | string | enum: "high", "medium", "low" | `null` | Yes | Yes | Task priority level |
| `tags` | array[string] | max 20 items, max 50 chars/item | `[]` | No | GIN | Task categorization tags |

### Validation Rules

**priority**:
- **Allowed values**: "high", "medium", "low", null
- **Case-sensitive**: Must be lowercase
- **Validation**: Reject any value not in allowed set
- **Nullability**: null is valid (means "no priority")

**tags**:
- **Type**: JSON array of strings
- **Max items**: 20 tags per task
- **Max length per tag**: 50 characters
- **Trimming**: Leading/trailing whitespace automatically removed
- **Empty tags**: Rejected (must have at least 1 non-whitespace character)
- **Deduplication**: Automatic (case-sensitive: "Work" ≠ "work")
- **Order**: Preserved as provided by user
- **Nullability**: Never null (use empty array `[]` instead)

---

## Database Schema (PostgreSQL)

### Table: `tasks` (Level 2 Extensions)

```sql
-- Add Level 2 columns to existing tasks table
ALTER TABLE tasks
  ADD COLUMN priority VARCHAR(10) DEFAULT NULL,
  ADD COLUMN tags JSONB NOT NULL DEFAULT '[]'::jsonb;

-- Add indexes for Level 2 features
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_tags ON tasks USING GIN(tags);

-- Add check constraint for priority enum
ALTER TABLE tasks
  ADD CONSTRAINT check_priority_enum
  CHECK (priority IS NULL OR priority IN ('high', 'medium', 'low'));
```

### Complete Table Definition (After Level 2 Migration)

```sql
CREATE TABLE tasks (
    -- Level 1 fields
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL CHECK (length(trim(title)) > 0),
    description VARCHAR(1000) DEFAULT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Level 2 fields (NEW)
    priority VARCHAR(10) DEFAULT NULL CHECK (priority IS NULL OR priority IN ('high', 'medium', 'low')),
    tags JSONB NOT NULL DEFAULT '[]'::jsonb,

    -- Level 3 fields (deferred)
    -- due_date TIMESTAMP DEFAULT NULL,
    -- recurrence VARCHAR(20) DEFAULT NULL,
    -- reminder_time TIMESTAMP DEFAULT NULL
);

-- Indexes (Level 1)
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
CREATE INDEX idx_tasks_completed ON tasks(completed);

-- Indexes (Level 2 - NEW)
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_tags ON tasks USING GIN(tags);

-- Trigger for updated_at (Level 1, unchanged)
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

## Pydantic Schemas for API (Level 2)

### TaskCreate (Extended)

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List

class TaskCreate(BaseModel):
    """Schema for creating a new task with Level 2 fields"""

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

    priority: Optional[str] = Field(
        default=None,
        description="Task priority: high, medium, low, or null"
    )

    tags: List[str] = Field(
        default_factory=list,
        description="Task tags (max 20 tags, max 50 chars each)"
    )

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Task title cannot be empty or whitespace only')
        return v.strip()

    @validator('priority')
    def validate_priority(cls, v):
        if v is not None and v not in ['high', 'medium', 'low']:
            raise ValueError('Priority must be high, medium, low, or null')
        return v

    @validator('tags')
    def validate_tags(cls, v):
        if len(v) > 20:
            raise ValueError('Maximum 20 tags allowed')
        deduped = []
        seen = set()
        for tag in v:
            tag_stripped = tag.strip()
            if not tag_stripped:
                raise ValueError('Tags cannot be empty or whitespace only')
            if len(tag_stripped) > 50:
                raise ValueError(f'Tag "{tag_stripped}" exceeds 50 character limit')
            if tag_stripped not in seen:
                seen.add(tag_stripped)
                deduped.append(tag_stripped)
        return deduped

    class Config:
        schema_extra = {
            "example": {
                "title": "Deploy application",
                "description": "Deploy to staging environment",
                "priority": "high",
                "tags": ["work", "urgent", "deployment"]
            }
        }
```

### TaskUpdate (Extended)

```python
class TaskUpdate(BaseModel):
    """Schema for updating a task with Level 2 fields (partial updates allowed)"""

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

    priority: Optional[str] = Field(
        default=None,
        description="Updated priority (null to remove)"
    )

    tags: Optional[List[str]] = Field(
        default=None,
        description="Updated tags (replaces all existing tags)"
    )

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Task title cannot be empty or whitespace only')
        return v.strip() if v else v

    @validator('priority')
    def validate_priority(cls, v):
        if v is not None and v not in ['high', 'medium', 'low']:
            raise ValueError('Priority must be high, medium, low, or null')
        return v

    @validator('tags')
    def validate_tags(cls, v):
        if v is None:
            return None
        if len(v) > 20:
            raise ValueError('Maximum 20 tags allowed')
        deduped = []
        seen = set()
        for tag in v:
            tag_stripped = tag.strip()
            if not tag_stripped:
                raise ValueError('Tags cannot be empty or whitespace only')
            if len(tag_stripped) > 50:
                raise ValueError(f'Tag "{tag_stripped}" exceeds 50 character limit')
            if tag_stripped not in seen:
                seen.add(tag_stripped)
                deduped.append(tag_stripped)
        return deduped

    class Config:
        schema_extra = {
            "example": {
                "priority": "medium",
                "tags": ["work", "deployment"]
            }
        }
```

### TaskResponse (Extended)

```python
class TaskResponse(BaseModel):
    """Schema for task responses (read operations) with Level 2 fields"""

    id: UUID
    title: str
    description: Optional[str]
    completed: bool
    priority: Optional[str]          # NEW
    tags: List[str]                  # NEW
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Deploy application",
                "description": "Deploy to staging environment",
                "completed": False,
                "priority": "high",
                "tags": ["work", "urgent", "deployment"],
                "created_at": "2026-01-09T10:30:00.000Z",
                "updated_at": "2026-01-09T10:30:00.000Z"
            }
        }
```

---

## Database Migration Strategy

### Migration: Add Level 2 Fields

```python
# alembic/versions/002_add_organization_fields.py
"""Add priority and tags fields (Level 2)

Revision ID: 002
Revises: 001
Create Date: 2026-01-09

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Add priority column
    op.add_column('tasks',
        sa.Column('priority', sa.String(10), nullable=True)
    )

    # Add tags column with default empty array
    op.add_column('tasks',
        sa.Column('tags', postgresql.JSONB(), nullable=False, server_default="'[]'::jsonb")
    )

    # Add check constraint for priority enum
    op.create_check_constraint(
        'check_priority_enum',
        'tasks',
        "priority IS NULL OR priority IN ('high', 'medium', 'low')"
    )

    # Create indexes
    op.create_index('idx_tasks_priority', 'tasks', ['priority'])
    op.create_index('idx_tasks_tags', 'tasks', ['tags'], postgresql_using='gin')

def downgrade():
    # Drop indexes
    op.drop_index('idx_tasks_tags', table_name='tasks')
    op.drop_index('idx_tasks_priority', table_name='tasks')

    # Drop check constraint
    op.drop_constraint('check_priority_enum', 'tasks')

    # Drop columns
    op.drop_column('tasks', 'tags')
    op.drop_column('tasks', 'priority')
```

### Data Migration Verification

After migration, verify:

```sql
-- Check that all existing tasks have default values
SELECT
  COUNT(*) AS total_tasks,
  COUNT(*) FILTER (WHERE priority IS NULL) AS no_priority,
  COUNT(*) FILTER (WHERE tags = '[]'::jsonb) AS no_tags
FROM tasks;

-- Expected: all tasks have priority = NULL and tags = []
```

---

## Schema Evolution Principles (Level 2)

1. **Additive Only**: No columns removed from Level 1
2. **Nullable New Fields**: `priority` is nullable for backward compatibility
3. **Default Values**: `tags` defaults to `[]` (empty array, never null)
4. **No Breaking Changes**: Level 1 apps continue to work without modification
5. **Indexes Added**: GIN index on `tags` for efficient array queries
6. **Check Constraints**: Priority enum enforced at database level

---

## Data Integrity Constraints

### Database-Level Constraints (Level 2 Additions)

- `priority` CHECK constraint (enum validation)
- `tags` NOT NULL (must be array, can be empty)
- `tags` GIN index for array containment queries (`@>` operator)

### Application-Level Validation (Pydantic - Level 2)

- Priority enum validation ("high", "medium", "low", null only)
- Tags array max length (20 items)
- Individual tag max length (50 characters)
- Tag deduplication (case-sensitive)
- Tag trimming (whitespace removal)
- Empty tag rejection

---

## Query Performance Optimizations

### Index Usage

**Priority Index** (`idx_tasks_priority`):
- Used for: Filtering by priority, sorting by priority
- Query: `WHERE priority = 'high'`
- Query: `ORDER BY priority`

**Tags GIN Index** (`idx_tasks_tags`):
- Used for: Tag containment queries
- Query: `WHERE tags @> ARRAY['work']::text[]` (has tag "work")
- Query: `WHERE tags @> ARRAY['work', 'urgent']::text[]` (has both tags)

**Combined Queries**:
```sql
-- Efficient query using both indexes
SELECT * FROM tasks
WHERE priority = 'high'
  AND tags @> ARRAY['work']::text[]
  AND completed = false
ORDER BY created_at DESC;
```

### Query Plans

```sql
-- Analyze query performance
EXPLAIN ANALYZE
SELECT * FROM tasks
WHERE priority = 'high' AND tags @> ARRAY['work', 'urgent']::text[];
```

---

## Backward Compatibility Guarantees

### For Level 1 Applications

1. **Schema Compatibility**:
   - All Level 1 fields remain unchanged
   - New fields are nullable or have defaults
   - No data loss or corruption

2. **Query Compatibility**:
   - Level 1 queries continue to work
   - New fields appear in results but can be ignored

3. **Insertion Compatibility**:
   - Inserting without `priority` or `tags` works (defaults applied)

4. **Update Compatibility**:
   - Updating without touching `priority` or `tags` works (fields unchanged)

### Migration Safety

```sql
-- Test backward compatibility after migration
-- This Level 1 query should still work:
SELECT id, title, description, completed, created_at, updated_at
FROM tasks
WHERE completed = false
ORDER BY created_at DESC;

-- This Level 1 insert should still work:
INSERT INTO tasks (id, title, description, completed, created_at, updated_at)
VALUES (gen_random_uuid(), 'Test task', 'Description', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
-- Expected: priority = NULL, tags = []
```

---

## Testing Data

### Seed Data (Level 2)

```python
from uuid import uuid4
from datetime import datetime

seed_tasks_level2 = [
    {
        "id": uuid4(),
        "title": "Deploy application to staging",
        "description": "Deploy version 2.0",
        "completed": False,
        "priority": "high",
        "tags": ["work", "urgent", "deployment"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": uuid4(),
        "title": "Write documentation",
        "description": "Update API docs",
        "completed": False,
        "priority": "medium",
        "tags": ["work", "documentation"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": uuid4(),
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": False,
        "priority": None,  # No priority
        "tags": [],  # No tags
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": uuid4(),
        "title": "Review pull request",
        "description": "Review PR #123",
        "completed": True,
        "priority": "low",
        "tags": ["work", "review"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]
```

---

## Constitutional Compliance

✅ **Additive Only**: No Level 1 fields removed or renamed
✅ **Backward Compatible**: Level 1 apps continue to work
✅ **Schema Evolution**: Nullable fields for future compatibility
✅ **Database Constraints**: Enforced at DB level (priority enum, tags validation)
✅ **Performance**: Indexes for efficient querying
✅ **Data Integrity**: Validation at both DB and application layers
