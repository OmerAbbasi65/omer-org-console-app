# API Contract: Level 2 (Organization) Extensions

**Version**: 2.0.0
**Base URL**: `/api/v1`
**Content-Type**: `application/json`
**Phase**: Phase 2 - Level 2 (Organization Features)
**Date**: 2026-01-09

## Overview

This document defines REST API extensions for Level 2 (Organization) features. All Level 1 endpoints remain unchanged and fully backward compatible.

## Changes from Level 1

### Modified Endpoints

All Level 1 endpoints now return additional fields:
- `priority`: string | null
- `tags`: string[] (never null, defaults to empty array)

### New Query Parameters

GET `/api/v1/tasks` now supports filtering, sorting, and search via query parameters.

---

## Endpoint Extensions

### 1. Create Task (Extended)

**POST** `/api/v1/tasks`

**Request Body** (Level 2 additions):

```json
{
  "title": "Deploy application",
  "description": "Deploy to staging environment",
  "priority": "high",          // NEW: optional, "high"|"medium"|"low"|null
  "tags": ["work", "urgent"]   // NEW: optional, array of strings
}
```

**Schema Validation** (Level 2 additions):
- `priority` (optional, enum: "high" | "medium" | "low" | null)
- `tags` (optional, array of strings, max 20 items, max 50 chars per item)

**Success Response (201 Created)**:

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Deploy application",
    "description": "Deploy to staging environment",
    "completed": false,
    "priority": "high",          // NEW
    "tags": ["work", "urgent"],  // NEW
    "createdAt": "2026-01-09T10:30:00.000Z",
    "updatedAt": "2026-01-09T10:30:00.000Z"
  }
}
```

**Error Responses** (Level 2 additions):

**422 Unprocessable Entity** - Invalid priority value
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Priority must be one of: high, medium, low, or null",
    "details": {
      "field": "priority",
      "constraint": "enum",
      "allowedValues": ["high", "medium", "low", null]
    }
  }
}
```

**422 Unprocessable Entity** - Too many tags
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Maximum 20 tags allowed per task",
    "details": {
      "field": "tags",
      "constraint": "max-length",
      "limit": 20,
      "provided": 25
    }
  }
}
```

**422 Unprocessable Entity** - Tag too long
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Tag exceeds maximum length of 50 characters",
    "details": {
      "field": "tags",
      "constraint": "max-string-length",
      "limit": 50,
      "tag": "this-is-a-very-long-tag-name-that-exceeds-the-fifty-character-limit-for-tags"
    }
  }
}
```

---

### 2. Get All Tasks (Extended with Filtering, Sorting, Search)

**GET** `/api/v1/tasks`

**Query Parameters** (Level 2 additions):

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `status` | string | Filter by completion status | `?status=incomplete` |
| `priority` | string | Filter by priority level | `?priority=high` |
| `tag` | string | Filter by tag (can repeat for AND logic) | `?tag=work&tag=urgent` |
| `search` | string | Search in title and description | `?search=groceries` |
| `sortBy` | string | Sort field | `?sortBy=priority` |
| `order` | string | Sort order (asc/desc) | `?order=desc` |

**Query Parameter Details**:

**status**:
- Values: `completed` | `incomplete`
- Effect: Returns only tasks matching the specified completion status
- Example: `?status=incomplete` (only incomplete tasks)

**priority**:
- Values: `high` | `medium` | `low` | `none`
- Effect: Returns only tasks with the specified priority
- Special: `none` matches tasks with `priority = null`
- Example: `?priority=high` (only high-priority tasks)

**tag**:
- Values: Any string
- Effect: Returns tasks that have ALL specified tags (AND logic)
- Multiple: Repeat parameter for multiple tags
- Example: `?tag=work&tag=urgent` (tasks with BOTH "work" AND "urgent")

**search**:
- Values: Any string
- Effect: Case-insensitive partial match in `title` and `description`
- Example: `?search=gro` (matches "Buy groceries", "Grow plants", etc.)

**sortBy**:
- Values: `priority` | `title` | `createdAt` | `updatedAt`
- Default: `createdAt`
- Effect: Field to sort by

**order**:
- Values: `asc` | `desc`
- Default: `desc` for `createdAt`, `asc` for others
- Effect: Sort direction

**Success Response (200 OK)**:

```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Deploy application",
        "description": "Deploy to staging environment",
        "completed": false,
        "priority": "high",
        "tags": ["work", "urgent"],
        "createdAt": "2026-01-09T10:30:00.000Z",
        "updatedAt": "2026-01-09T10:30:00.000Z"
      },
      {
        "id": "660e8400-e29b-41d4-a716-446655440001",
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": false,
        "priority": null,
        "tags": [],
        "createdAt": "2026-01-09T09:15:00.000Z",
        "updatedAt": "2026-01-09T09:15:00.000Z"
      }
    ],
    "total": 2,
    "filters": {                    // NEW: Applied filters
      "status": "incomplete",
      "priority": null,
      "tags": [],
      "search": null
    },
    "sort": {                       // NEW: Applied sort
      "by": "createdAt",
      "order": "desc"
    }
  }
}
```

**Empty Result**:
```json
{
  "success": true,
  "data": {
    "tasks": [],
    "total": 0,
    "filters": {
      "status": "incomplete",
      "priority": "high",
      "tags": ["work", "urgent"],
      "search": "nonexistent"
    },
    "sort": {
      "by": "priority",
      "order": "desc"
    }
  }
}
```

**Example Queries**:

```bash
# Filter by status
GET /api/v1/tasks?status=incomplete

# Filter by priority
GET /api/v1/tasks?priority=high

# Filter by multiple tags (AND logic)
GET /api/v1/tasks?tag=work&tag=urgent

# Search for keyword
GET /api/v1/tasks?search=groceries

# Composite: incomplete high-priority work tasks
GET /api/v1/tasks?status=incomplete&priority=high&tag=work

# Sort by priority (high to low)
GET /api/v1/tasks?sortBy=priority&order=desc

# Sort by title alphabetically
GET /api/v1/tasks?sortBy=title&order=asc

# Full example: search + filter + sort
GET /api/v1/tasks?search=deploy&status=incomplete&priority=high&sortBy=createdAt&order=desc
```

**Error Responses**:

**400 Bad Request** - Invalid status value
```json
{
  "success": false,
  "error": {
    "code": "INVALID_QUERY_PARAMETER",
    "message": "Invalid status value. Must be 'completed' or 'incomplete'",
    "details": {
      "parameter": "status",
      "provided": "in-progress"
    }
  }
}
```

**400 Bad Request** - Invalid priority value
```json
{
  "success": false,
  "error": {
    "code": "INVALID_QUERY_PARAMETER",
    "message": "Invalid priority value. Must be 'high', 'medium', 'low', or 'none'",
    "details": {
      "parameter": "priority",
      "provided": "critical"
    }
  }
}
```

**400 Bad Request** - Invalid sortBy field
```json
{
  "success": false,
  "error": {
    "code": "INVALID_QUERY_PARAMETER",
    "message": "Invalid sortBy field. Must be 'priority', 'title', 'createdAt', or 'updatedAt'",
    "details": {
      "parameter": "sortBy",
      "provided": "dueDate"
    }
  }
}
```

---

### 3. Update Task (Extended)

**PATCH** `/api/v1/tasks/{taskId}`

**Request Body** (Level 2 additions):

```json
{
  "title": "Deploy application to production",
  "description": "Updated description",
  "priority": "medium",          // NEW: optional
  "tags": ["work", "deployment"] // NEW: optional (replaces all tags)
}
```

**Schema Validation** (Level 2 additions):
- `priority` (optional, enum: "high" | "medium" | "low" | null)
- `tags` (optional, array of strings, replaces existing tags entirely)

**Success Response (200 OK)**:

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Deploy application to production",
    "description": "Updated description",
    "completed": false,
    "priority": "medium",
    "tags": ["work", "deployment"],
    "createdAt": "2026-01-09T10:30:00.000Z",
    "updatedAt": "2026-01-09T12:45:00.000Z"  // Updated timestamp
  }
}
```

**Notes**:
- Updating `tags` replaces the entire array (not append/remove)
- To remove all tags, send `"tags": []`
- To remove priority, send `"priority": null`
- Omitting `priority` or `tags` leaves them unchanged

---

### 4. Get Single Task (Extended)

**GET** `/api/v1/tasks/{taskId}`

**Success Response (200 OK)**:

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Deploy application",
    "description": "Deploy to staging environment",
    "completed": false,
    "priority": "high",          // NEW
    "tags": ["work", "urgent"],  // NEW
    "createdAt": "2026-01-09T10:30:00.000Z",
    "updatedAt": "2026-01-09T10:30:00.000Z"
  }
}
```

---

### 5. Toggle Task Completion (Unchanged)

**PATCH** `/api/v1/tasks/{taskId}/toggle`

**No changes from Level 1**, but response includes Level 2 fields:

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Deploy application",
    "description": "Deploy to staging environment",
    "completed": true,           // Toggled
    "priority": "high",
    "tags": ["work", "urgent"],
    "createdAt": "2026-01-09T10:30:00.000Z",
    "updatedAt": "2026-01-09T14:20:00.000Z"
  }
}
```

---

### 6. Delete Task (Unchanged)

**DELETE** `/api/v1/tasks/{taskId}`

**No changes from Level 1**.

---

## Sort Order Specifications

### Priority Sort

Order: `high` → `medium` → `low` → `null`

**Ascending** (`?sortBy=priority&order=asc`):
1. High priority tasks
2. Medium priority tasks
3. Low priority tasks
4. No priority tasks (null)

**Descending** (`?sortBy=priority&order=desc`):
1. No priority tasks (null)
2. Low priority tasks
3. Medium priority tasks
4. High priority tasks

**Tie-breaking**: When priorities are equal, sort by `createdAt desc` (newest first)

### Title Sort

**Ascending** (`?sortBy=title&order=asc`): A → Z (case-insensitive)
**Descending** (`?sortBy=title&order=desc`): Z → A (case-insensitive)

**Tie-breaking**: Not applicable (titles are unique-enough in practice)

### Created Date Sort

**Ascending** (`?sortBy=createdAt&order=asc`): Oldest first
**Descending** (`?sortBy=createdAt&order=desc`): Newest first (default)

### Updated Date Sort

**Ascending** (`?sortBy=updatedAt&order=asc`): Least recently updated first
**Descending** (`?sortBy=updatedAt&order=desc`): Most recently updated first

---

## Filter Logic Specifications

### AND Logic for Multiple Filters

When multiple filter parameters are provided, ALL conditions must match (AND logic).

**Example**:
```
GET /api/v1/tasks?status=incomplete&priority=high&tag=work&tag=urgent
```

**Matches**:
- Tasks that are **incomplete** AND
- Tasks with priority **"high"** AND
- Tasks with tag **"work"** AND
- Tasks with tag **"urgent"**

### Tag Filtering (Multiple Tags)

Multiple `tag` parameters use AND logic (task must have ALL tags).

**Example**:
```
GET /api/v1/tasks?tag=work&tag=urgent
```

**Matches**: Tasks with BOTH "work" AND "urgent" tags
**Does NOT Match**: Tasks with only "work" or only "urgent"

### Priority "none" Filter

**Example**:
```
GET /api/v1/tasks?priority=none
```

**Matches**: Tasks where `priority IS NULL`

---

## Search Specifications

### Search Algorithm

1. Case-insensitive matching
2. Partial substring matching (contains)
3. Searches in `title` and `description` fields
4. Single keyword only (no boolean operators in Level 2)

### Search Examples

**Query**: `?search=gro`
**Matches**:
- "Buy **gro**ceries"
- "**Gro**w plants"
- Description: "Organic **gro**wth strategy"

**Query**: `?search=URGENT`
**Matches** (case-insensitive):
- "**Urgent** task"
- "This is **urgent**"

### Search Edge Cases

**Empty search**: `?search=` (empty string) → Returns all tasks (no filtering)
**Whitespace search**: `?search=%20%20%20` → Returns all tasks (trimmed to empty)
**Special characters**: Escaped and matched literally (no regex interpretation)

---

## Backward Compatibility Guarantees

### Level 1 Clients

Level 1 clients (not aware of Level 2 features) MUST continue to work:

1. **Create Task without Level 2 fields**:
   ```json
   POST /api/v1/tasks
   {"title": "Task", "description": "Desc"}
   ```
   Result: `priority = null`, `tags = []`

2. **Get Tasks without query parameters**:
   ```
   GET /api/v1/tasks
   ```
   Result: All tasks returned with default sort (`createdAt desc`)

3. **Update Task without Level 2 fields**:
   ```json
   PATCH /api/v1/tasks/{id}
   {"title": "Updated"}
   ```
   Result: Only title updated, `priority` and `tags` unchanged

4. **Response Structure**:
   Level 1 clients MUST ignore `priority` and `tags` fields if they don't recognize them.

---

## Performance Requirements

- **Search**: < 2 seconds for 1000 tasks
- **Filter**: < 1 second for 1000 tasks
- **Sort**: < 500ms for 1000 tasks
- **Composite (search + filter + sort)**: < 2 seconds for 1000 tasks

---

## Database Query Patterns

### Filtering

```sql
-- Filter by status
WHERE completed = false

-- Filter by priority
WHERE priority = 'high'

-- Filter by priority "none"
WHERE priority IS NULL

-- Filter by tag (single)
WHERE tags @> ARRAY['work']::text[]

-- Filter by multiple tags (AND logic)
WHERE tags @> ARRAY['work', 'urgent']::text[]
```

### Search

```sql
-- Search in title and description (case-insensitive)
WHERE LOWER(title) LIKE LOWER('%groceries%')
   OR LOWER(description) LIKE LOWER('%groceries%')
```

### Sorting

```sql
-- Sort by priority (high to low)
ORDER BY
  CASE priority
    WHEN 'high' THEN 1
    WHEN 'medium' THEN 2
    WHEN 'low' THEN 3
    ELSE 4
  END ASC,
  created_at DESC

-- Sort by title (A-Z)
ORDER BY LOWER(title) ASC

-- Sort by created date (newest first)
ORDER BY created_at DESC
```

---

## Error Code Reference (Level 2 Additions)

| Error Code | HTTP Status | Description |
|------------|-------------|-------------|
| `INVALID_QUERY_PARAMETER` | 400 | Query parameter value is invalid |
| `TAG_LIMIT_EXCEEDED` | 422 | More than 20 tags provided |
| `TAG_TOO_LONG` | 422 | Tag exceeds 50 characters |
| `INVALID_PRIORITY` | 422 | Priority value not in allowed set |

---

## OpenAPI / Swagger

Updated OpenAPI spec available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

Level 2 query parameters are fully documented in the interactive API docs.

---

## Testing Examples (cURL)

### Create Task with Priority and Tags

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Deploy application",
    "description": "Deploy to staging",
    "priority": "high",
    "tags": ["work", "urgent", "deployment"]
  }'
```

### Search Tasks

```bash
curl "http://localhost:8000/api/v1/tasks?search=groceries"
```

### Filter by Priority

```bash
curl "http://localhost:8000/api/v1/tasks?priority=high"
```

### Filter by Multiple Tags

```bash
curl "http://localhost:8000/api/v1/tasks?tag=work&tag=urgent"
```

### Composite Query

```bash
curl "http://localhost:8000/api/v1/tasks?status=incomplete&priority=high&tag=work&sortBy=priority&order=desc"
```

### Update Priority and Tags

```bash
curl -X PATCH http://localhost:8000/api/v1/tasks/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "priority": "medium",
    "tags": ["work", "deployment"]
  }'
```

---

## Constitutional Compliance

✅ **Spec-First**: API designed before implementation
✅ **Backward Compatible**: Level 1 clients continue to work
✅ **Progressive Maturity**: Builds on Level 1 without breaking it
✅ **Additive Only**: No removed endpoints or fields
✅ **Clear Contracts**: All behaviors explicitly documented
