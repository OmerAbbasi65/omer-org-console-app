# Data Model: AI-Native Todo Console Application

**Feature**: 001-todo-app-full
**Date**: 2026-01-01
**Status**: Approved

## Purpose

Define the canonical data structures for the Todo application, ensuring alignment with constitutional requirements and specification.

## Core Entities

### Task

Represents a single todo item with all metadata required across Basic, Intermediate, and Advanced feature levels.

**Schema** (JSON representation):

```json
{
  "id": "string",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "priority": "high" | "medium" | "low" | null,
  "tags": ["string"],
  "dueDate": "string (ISO-8601) | null",
  "recurrence": "none" | "daily" | "weekly" | "monthly",
  "reminderTime": "string (ISO-8601) | null",
  "lastNotified": "string (ISO-8601) | null",
  "createdAt": "string (ISO-8601)",
  "updatedAt": "string (ISO-8601)"
}
```

**Field Specifications**:

| Field | Type | Required | Level | Description | Validation Rules |
|-------|------|----------|-------|-------------|------------------|
| `id` | string | Yes | Basic | Unique identifier | Format: `task-<unix-timestamp-ms>`, generated at creation |
| `title` | string | Yes | Basic | Task title | Non-empty, max 500 characters |
| `description` | string\|null | No | Basic | Extended task description | Max 5000 characters, defaults to `null` |
| `completed` | boolean | Yes | Basic | Completion status | Must be `true` or `false`, never `null`, defaults to `false` |
| `priority` | enum\|null | No | Intermediate | Task priority | One of: `"high"`, `"medium"`, `"low"`, or `null` |
| `tags` | string[] | No | Intermediate | Categorization tags | Array of strings, defaults to `[]`, each tag max 50 chars |
| `dueDate` | string\|null | No | Advanced | When task is due | ISO-8601 datetime, validated format, defaults to `null` |
| `recurrence` | enum | No | Advanced | Recurring pattern | One of: `"none"`, `"daily"`, `"weekly"`, `"monthly"`, defaults to `"none"` |
| `reminderTime` | string\|null | No | Advanced | When to send reminder | ISO-8601 datetime, must be before `dueDate` if both set, defaults to `null` |
| `lastNotified` | string\|null | No | Advanced | Last reminder notification time | ISO-8601 datetime, system-managed, defaults to `null` |
| `createdAt` | string | Yes | Basic | Creation timestamp | ISO-8601 datetime, set automatically at creation, immutable |
| `updatedAt` | string | Yes | Basic | Last modification timestamp | ISO-8601 datetime, updated automatically on any change |

**Invariants**:

1. `id` must be unique across all tasks
2. `completed` must never be `null` (boolean constraint)
3. If `reminderTime` is set, `dueDate` must also be set
4. If `recurrence != "none"`, `dueDate` must be set
5. `createdAt` must never change after creation
6. `updatedAt` must update on every modification
7. If `priority` is set, must be one of the three allowed values

**State Transitions**:

```
Task Creation:
  → id = generateTimestampId()
  → completed = false
  → createdAt = now()
  → updatedAt = now()
  → all other fields per user input or defaults

Task Update (title/description):
  → updatedAt = now()
  → specified fields updated

Task Completion:
  IF recurrence == "none":
    → completed = true
    → updatedAt = now()
  IF recurrence != "none":
    → dueDate = calculateNextDueDate(dueDate, recurrence)
    → completed = false (reset)
    → reminderTime = null (reset)
    → lastNotified = null (reset)
    → updatedAt = now()

Task Deletion:
  → Remove from storage permanently
```

---

## Derived Models

### TaskFilter

Criteria for filtering tasks (used in filter/search operations).

```json
{
  "status": "complete" | "incomplete" | null,
  "priority": "high" | "medium" | "low" | null,
  "tag": "string | null",
  "keyword": "string | null"
}
```

**Behavior**:
- All non-null fields are combined with AND logic
- `keyword`: case-insensitive partial match against `title` and `description`
- `tag`: matches if task's `tags` array contains the specified tag
- `status`: maps to `completed` boolean (`"complete"` → `true`, `"incomplete"` → `false`)

---

### TaskSort

Sorting specification for task lists.

```json
{
  "field": "priority" | "title" | "dueDate" | "createdAt",
  "direction": "asc" | "desc"
}
```

**Sort Ordering**:
- **priority**: `"high"` > `"medium"` > `"low"` > `null` (descending), or reverse (ascending)
- **title**: Alphabetical (case-insensitive)
- **dueDate**: Chronological, `null` values last
- **createdAt**: Chronological (timestamp order)

---

## Storage Model

### File Format

Tasks are persisted as a JSON array in `~/.todo-data.json`:

```json
[
  {
    "id": "task-1735707600000",
    "title": "Buy groceries",
    "description": null,
    "completed": false,
    "priority": null,
    "tags": [],
    "dueDate": null,
    "recurrence": "none",
    "reminderTime": null,
    "lastNotified": null,
    "createdAt": "2026-01-01T12:00:00Z",
    "updatedAt": "2026-01-01T12:00:00Z"
  }
]
```

**File Characteristics**:
- **Pretty-printed**: 2-space indentation for human readability
- **UTF-8 encoded**
- **Atomic writes**: Write to `.todo-data.json.tmp`, then rename to prevent corruption
- **Empty state**: Empty array `[]` if no tasks exist

---

## Validation Rules

### On Task Creation

1. Validate `title` is non-empty and ≤ 500 characters
2. Validate `description` ≤ 5000 characters if provided
3. Validate `priority` is one of allowed values if provided
4. Validate `tags` array elements are ≤ 50 characters each
5. Validate `dueDate` is valid ISO-8601 if provided
6. Validate `recurrence` is one of allowed values
7. Validate `reminderTime` ≤ `dueDate` if both provided
8. Generate `id` = `task-<currentTimestampMs>()`
9. Set `createdAt` = `updatedAt` = current ISO-8601 timestamp
10. Set `completed` = `false`

### On Task Update

1. Validate task with given `id` exists
2. Apply same validation rules as creation for modified fields
3. Update `updatedAt` = current ISO-8601 timestamp
4. Preserve `id` and `createdAt` (immutable)

### On File Load

1. Validate JSON is parsable
2. Validate root is an array
3. Validate each element matches Task schema
4. If validation fails, log error and treat as empty array (graceful degradation)

---

## Evolution Strategy

**Backward Compatibility**:
- New fields must have default values
- Old field removal requires migration script
- Field type changes require versioning

**Migration Path** (if needed in future):
1. Add `version` field to root JSON structure
2. Implement migration functions for each version bump
3. Run migrations on load before returning tasks

**Example Future Migration**:
```json
{
  "version": 2,
  "tasks": [...]
}
```

---

## Alignment with Constitution

**Principle II - AI-Native Design**: Tasks represented as structured JSON, enabling agent introspection and manipulation.

**Principle V - Data Model Evolution**: Schema defined with optional fields (marked with `| null`), backward-compatible defaults, and clear evolution strategy.

**NFR-006**: JSON format is human-readable as required.

**FR-002**: ID format `task-<unix-timestamp-ms>` as specified.

**FR-009**: `completed` field is boolean, never null.

**FR-010**: Storage in `~/.todo-data.json` in user's home directory.
