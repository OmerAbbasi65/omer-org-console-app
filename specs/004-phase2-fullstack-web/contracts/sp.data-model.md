# Data Model: Phase 2 Todo Web Application

**Feature**: 004-phase2-fullstack-web
**Created**: 2026-01-09
**ORM**: SQLModel (Pydantic + SQLAlchemy)
**Database**: Neon Serverless PostgreSQL
**Schema Version**: 1.0.0

## Schema Authority

SQLModel is the canonical schema definition. All schema changes MUST:
1. Start with conceptual model update (this document)
2. Create migration specification
3. Generate Alembic migration
4. Apply to database
5. Update code to use new schema

## Core Principles

- **Backward Compatibility**: Only additive schema changes allowed; deprecate and migrate for removals
- **Timezone Discipline**: All timestamps stored as UTC (`TIMESTAMP WITH TIME ZONE`)
- **Global Uniqueness**: Primary keys use UUID v4 for global uniqueness
- **Soft Deletes**: No hard deletes in Phase 2; use `deleted_at` field (future consideration)
- **Audit Trail**: All tables include `created_at` and `updated_at` timestamps

---

## Task Model

The core entity representing a single todo item.

### Fields

| Field Name    | Type                  | Required | Default       | Constraints                          | Description                                    |
|---------------|-----------------------|----------|---------------|--------------------------------------|------------------------------------------------|
| `id`          | UUID                  | Yes      | uuid.uuid4()  | Primary key, unique                  | Globally unique task identifier                |
| `title`       | VARCHAR(200)          | Yes      | -             | NOT NULL, length 1-200               | Task title                                     |
| `description` | TEXT                  | No       | NULL          | Max 2000 chars (app-level validation)| Optional detailed description                  |
| `completed`   | BOOLEAN               | Yes      | FALSE         | NOT NULL                             | Completion status                              |
| `priority`    | ENUM                  | Yes      | 'medium'      | NOT NULL, one of: high, medium, low  | Priority level                                 |
| `tags`        | ARRAY[VARCHAR(50)]    | Yes      | []            | Max 10 items (app-level validation)  | Categorization tags                            |
| `due_date`    | TIMESTAMP WITH TZ     | No       | NULL          | -                                    | When task is due (UTC)                         |
| `recurrence`  | ENUM                  | Yes      | 'none'        | NOT NULL, one of: none, daily, weekly, monthly | Recurrence pattern                   |
| `parent_id`   | UUID (FK)             | No       | NULL          | References tasks.id                  | Parent task for recurring instances (future)   |
| `created_at`  | TIMESTAMP WITH TZ     | Yes      | CURRENT_TS    | NOT NULL                             | Record creation time (UTC)                     |
| `updated_at`  | TIMESTAMP WITH TZ     | Yes      | CURRENT_TS    | NOT NULL, auto-update on modification| Last modification time (UTC)                   |

### Indexes

- **Primary Key**: `id` (UUID, clustered index)
- **Index on completed**: `idx_tasks_completed` for filtering by status
- **Index on due_date**: `idx_tasks_due_date` for overdue queries and sorting
- **Index on priority**: `idx_tasks_priority` for priority-based filtering
- **Composite Index**: `idx_tasks_status_priority` on (`completed`, `priority`) for common filter combinations
- **GIN Index on tags**: `idx_tasks_tags` for efficient tag array queries

### Constraints

- **Primary Key**: `pk_tasks` on `id`
- **Check Constraint**: `chk_title_not_empty` ensures `LENGTH(TRIM(title)) > 0`
- **Check Constraint**: `chk_priority_valid` ensures `priority IN ('high', 'medium', 'low')`
- **Check Constraint**: `chk_recurrence_valid` ensures `recurrence IN ('none', 'daily', 'weekly', 'monthly')`
- **Check Constraint**: `chk_recurrence_requires_due_date` ensures `recurrence = 'none' OR due_date IS NOT NULL`

### Relationships

- **Self-Referencing**: `parent_id` references `tasks.id` for recurring task instances (nullable, future use for tracking generated occurrences)

### Backward Compatibility Rules

- **v1.0.0**: Initial schema
- **Future additions**: New columns must be nullable or have defaults
- **Future removals**: Mark column as deprecated, migrate data, then remove in next MAJOR version
- **Enum expansions**: Adding new enum values is MINOR version; removing is MAJOR version

---

## Recurrence Model (Conceptual)

Recurrence logic is embedded in Task model via `recurrence` field. This conceptual model defines how recurrence behaves.

### Recurrence Patterns

| Pattern     | Meaning                                       | Next Occurrence Calculation                      |
|-------------|-----------------------------------------------|--------------------------------------------------|
| `none`      | Non-recurring task                            | N/A                                              |
| `daily`     | Repeats every day                             | `due_date + 1 day`                               |
| `weekly`    | Repeats every 7 days                          | `due_date + 7 days`                              |
| `monthly`   | Repeats on same day of month (or last day)    | `due_date + 1 month` (handle month-end edge cases)|

### Recurrence Logic Rules

1. **Anchor Point**: Original `due_date` is the anchor for calculating future occurrences
2. **Instance Generation**: When recurring task is marked complete:
   - Calculate next due date based on pattern
   - Create new task with same title, description, priority, tags, recurrence pattern
   - Set `parent_id` to original task's ID (for future traceability)
   - New task has `completed = FALSE` and fresh `created_at`
3. **Month-End Handling**: For monthly recurrence, if due day > days in target month, use last day of month (e.g., Jan 31 → Feb 28/29)
4. **No Retroactive Generation**: Only generate next single occurrence on completion; no bulk generation of missed occurrences
5. **Deletion Cascade**: Deleting parent task does NOT delete child occurrences (each is independent after creation)

### Storage

- No separate table for recurrence patterns in Phase 2
- Recurrence logic is application-layer responsibility (service or agent)
- `recurrence` ENUM field in Task table + `parent_id` for lineage tracking

---

## Reminder Model (Conceptual)

Reminders are conceptual in Phase 2; no separate database table. Reminder time is calculated on-demand from task metadata.

### Reminder Semantics

- **Trigger Time**: User specifies reminder as offset before `due_date` (e.g., "30 minutes before")
- **Storage**: Store `reminder_offset` (integer minutes) as nullable field in Task table (future addition)
- **Calculation**: `reminder_time = due_date - reminder_offset`
- **Notification**: When `current_time >= reminder_time AND current_time < due_date`, trigger notification
- **One-Time Only**: Each reminder triggers once; mark as `reminder_sent = TRUE` after notification

### Reminder Fields (Future Addition - Not in v1.0.0)

| Field Name        | Type      | Required | Default | Description                                    |
|-------------------|-----------|----------|---------|------------------------------------------------|
| `reminder_offset` | INTEGER   | No       | NULL    | Minutes before due_date to trigger reminder    |
| `reminder_sent`   | BOOLEAN   | No       | FALSE   | Whether reminder notification was sent         |

**Note**: Phase 2 may implement reminders without persistent storage via polling service that queries tasks with `due_date - reminder_offset <= current_time`.

---

## Schema Evolution Strategy

### Version Numbering

- **MAJOR.MINOR.PATCH** semantic versioning
- **MAJOR**: Breaking changes (column removal, type change, constraint tightening)
- **MINOR**: Additive changes (new column, new enum value, index addition)
- **PATCH**: Non-schema changes (documentation, constraint loosening)

### Migration Process

1. **Specification**: Document schema change in this file with version increment
2. **Review**: Constitutional compliance check (backward compatibility, timezone discipline)
3. **Migration Script**: Generate Alembic migration
4. **Testing**: Apply to test database, verify data integrity
5. **Deployment**: Apply to production during maintenance window
6. **Rollback Plan**: Document rollback steps for each migration

### Backward Compatibility Guarantee

- **No breaking changes in MINOR/PATCH versions**
- **All new columns nullable or have defaults**
- **Deprecation period**: 1 MAJOR version before removal
- **Data migration**: Automatic for additive changes; manual script for transformations

---

## Database Configuration

### Connection Settings

- **Database**: Neon Serverless PostgreSQL
- **Connection Pool**: Max 10 connections (Neon auto-scales)
- **Timeout**: 30 seconds for query execution
- **SSL**: Required (Neon enforces SSL)

### Character Encoding

- **Database Encoding**: UTF-8
- **Collation**: `en_US.UTF-8` (case-sensitive comparisons for tags, case-insensitive for search)

### Timezone Handling

- **Database Timezone**: UTC (enforced via `SET TIME ZONE 'UTC'` on connection)
- **Application Timezone**: All timestamps converted to UTC before storage
- **Display Timezone**: Frontend converts UTC to browser's local timezone

---

## Sample Data Models (Conceptual SQLModel Schemas)

### Task Schema (Conceptual)

```
Task:
  id: UUID (primary_key=True, default=uuid4)
  title: str (max_length=200, min_length=1)
  description: Optional[str] (max_length=2000)
  completed: bool (default=False)
  priority: Literal["high", "medium", "low"] (default="medium")
  tags: List[str] (default_factory=list, max_items=10)
  due_date: Optional[datetime] (timezone-aware, stored as UTC)
  recurrence: Literal["none", "daily", "weekly", "monthly"] (default="none")
  parent_id: Optional[UUID] (foreign_key="tasks.id")
  created_at: datetime (default=utc_now, timezone-aware)
  updated_at: datetime (default=utc_now, onupdate=utc_now, timezone-aware)
```

**Validation Rules**:
- `title`: stripped, non-empty after strip
- `description`: optional, max 2000 chars
- `tags`: unique values, max 10 items, each max 50 chars
- `due_date`: if `recurrence != 'none'`, due_date is required
- `priority`: must be one of enum values
- `recurrence`: must be one of enum values

---

## Data Integrity Rules

1. **Atomicity**: All task operations are atomic (single transaction)
2. **Consistency**: Foreign key constraints enforced (`parent_id` references valid task)
3. **Isolation**: Read Committed isolation level (default for Neon)
4. **Durability**: Neon handles durability (replicated storage)

---

## Query Patterns

### Common Queries

1. **Get all active tasks**: `SELECT * FROM tasks WHERE completed = FALSE ORDER BY created_at DESC`
2. **Get overdue tasks**: `SELECT * FROM tasks WHERE due_date < NOW() AND completed = FALSE`
3. **Filter by priority and tag**: `SELECT * FROM tasks WHERE priority = 'high' AND 'work' = ANY(tags)`
4. **Search by title**: `SELECT * FROM tasks WHERE LOWER(title) LIKE LOWER('%keyword%')`
5. **Get tasks due today**: `SELECT * FROM tasks WHERE DATE(due_date) = CURRENT_DATE`

### Performance Considerations

- Use indexes for frequent filters (priority, completed, due_date, tags)
- Pagination with `LIMIT/OFFSET` for large result sets
- Avoid `SELECT *` in production; specify required columns
- Use `EXPLAIN ANALYZE` for query optimization

---

## Soft Delete Strategy (Future Consideration)

Phase 2 uses hard deletes. Future phases may add:

- `deleted_at: Optional[datetime]` field
- Filter out deleted records in application layer (`WHERE deleted_at IS NULL`)
- Periodic cleanup job to purge old soft-deleted records

---

## Schema Version History

| Version | Date       | Changes                                                                 |
|---------|------------|-------------------------------------------------------------------------|
| 1.0.0   | 2026-01-09 | Initial schema: Task model with core fields, recurrence, indexes        |

---

## Notes

- **No User/Session Tables**: Phase 2 is single-user; no authentication tables
- **No Audit Log Table**: Use application-level logging; future may add `audit_log` table
- **No Attachment Support**: Tasks are text-only in Phase 2
- **No Collaboration Features**: No shared tasks, comments, or assignments in Phase 2
