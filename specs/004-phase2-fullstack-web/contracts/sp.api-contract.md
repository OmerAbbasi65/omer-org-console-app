# API Contract: Phase 2 Todo Web Application

**Feature**: 004-phase2-fullstack-web
**Created**: 2026-01-09
**Protocol**: RESTful HTTP/1.1 with JSON payloads
**Base URL**: `/api/v1`

## General Conventions

### Request/Response Format

- **Content-Type**: `application/json` for all requests and responses
- **Character Encoding**: UTF-8
- **Date/Time Format**: ISO-8601 with UTC timezone (`YYYY-MM-DDTHH:MM:SSZ`)
- **ID Format**: UUID v4 (e.g., `550e8400-e29b-41d4-a716-446655440000`)

### HTTP Methods

- **GET**: Retrieve resources (idempotent, no side effects)
- **POST**: Create new resources
- **PUT**: Update entire resource (replace)
- **PATCH**: Update partial resource (modify specific fields)
- **DELETE**: Remove resource (idempotent)

### Status Codes

- **200 OK**: Successful GET, PUT, PATCH
- **201 Created**: Successful POST with new resource created
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Invalid request payload or parameters
- **404 Not Found**: Resource not found
- **409 Conflict**: Resource conflict (e.g., duplicate ID)
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server-side error

### Error Response Schema

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable error description",
    "details": [
      {
        "field": "title",
        "issue": "Title cannot be empty"
      }
    ]
  }
}
```

**Error Codes**:
- `VALIDATION_ERROR`: Request payload failed validation
- `NOT_FOUND`: Requested resource does not exist
- `INTERNAL_ERROR`: Unexpected server error
- `CONFLICT`: Resource state conflict

---

## Level 1 - Core Task Management Endpoints

### POST /api/v1/tasks

Create a new task.

**Request Body**:
```json
{
  "title": "string (required, 1-200 chars)",
  "description": "string (optional, max 2000 chars)"
}
```

**Response** (201 Created):
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string | null",
  "completed": false,
  "priority": "medium",
  "tags": [],
  "dueDate": null,
  "recurrence": "none",
  "createdAt": "ISO-8601",
  "updatedAt": "ISO-8601"
}
```

**Errors**:
- `400`: Invalid JSON payload
- `422`: Validation error (title empty, title too long, description too long)

---

### GET /api/v1/tasks

Retrieve all tasks with optional filtering, sorting, and pagination.

**Query Parameters**:
- `status` (optional): `active` | `completed` | `all` (default: `all`)
- `priority` (optional): `high` | `medium` | `low`
- `tag` (optional): Single tag name (case-sensitive)
- `search` (optional): Search term for title/description (case-insensitive, partial match)
- `sortBy` (optional): `createdAt` | `dueDate` | `priority` | `title` (default: `createdAt`)
- `sortOrder` (optional): `asc` | `desc` (default: `desc`)
- `page` (optional): Page number, 1-indexed (default: 1)
- `limit` (optional): Items per page (default: 50, max: 100)

**Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": "uuid",
      "title": "string",
      "description": "string | null",
      "completed": boolean,
      "priority": "high | medium | low",
      "tags": ["string"],
      "dueDate": "ISO-8601 | null",
      "recurrence": "none | daily | weekly | monthly",
      "createdAt": "ISO-8601",
      "updatedAt": "ISO-8601"
    }
  ],
  "pagination": {
    "page": number,
    "limit": number,
    "total": number,
    "totalPages": number
  }
}
```

**Errors**:
- `400`: Invalid query parameters

---

### GET /api/v1/tasks/:id

Retrieve a single task by ID.

**Path Parameters**:
- `id`: Task UUID

**Response** (200 OK):
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string | null",
  "completed": boolean,
  "priority": "high | medium | low",
  "tags": ["string"],
  "dueDate": "ISO-8601 | null",
  "recurrence": "none | daily | weekly | monthly",
  "createdAt": "ISO-8601",
  "updatedAt": "ISO-8601"
}
```

**Errors**:
- `400`: Invalid UUID format
- `404`: Task not found

---

### PUT /api/v1/tasks/:id

Update an entire task (replace all fields).

**Path Parameters**:
- `id`: Task UUID

**Request Body**:
```json
{
  "title": "string (required, 1-200 chars)",
  "description": "string (optional, max 2000 chars)",
  "completed": boolean (required),
  "priority": "high | medium | low (required)",
  "tags": ["string"] (required, max 10 items),
  "dueDate": "ISO-8601 | null (required)",
  "recurrence": "none | daily | weekly | monthly (required)"
}
```

**Response** (200 OK):
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string | null",
  "completed": boolean,
  "priority": "high | medium | low",
  "tags": ["string"],
  "dueDate": "ISO-8601 | null",
  "recurrence": "none | daily | weekly | monthly",
  "createdAt": "ISO-8601",
  "updatedAt": "ISO-8601"
}
```

**Errors**:
- `400`: Invalid UUID format or JSON payload
- `404`: Task not found
- `422`: Validation error

---

### PATCH /api/v1/tasks/:id

Update specific fields of a task.

**Path Parameters**:
- `id`: Task UUID

**Request Body** (all fields optional):
```json
{
  "title": "string (1-200 chars)",
  "description": "string (max 2000 chars) | null",
  "completed": boolean,
  "priority": "high | medium | low",
  "tags": ["string"] (max 10 items),
  "dueDate": "ISO-8601 | null",
  "recurrence": "none | daily | weekly | monthly"
}
```

**Response** (200 OK):
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string | null",
  "completed": boolean,
  "priority": "high | medium | low",
  "tags": ["string"],
  "dueDate": "ISO-8601 | null",
  "recurrence": "none | daily | weekly | monthly",
  "createdAt": "ISO-8601",
  "updatedAt": "ISO-8601"
}
```

**Errors**:
- `400`: Invalid UUID format or JSON payload
- `404`: Task not found
- `422`: Validation error

---

### DELETE /api/v1/tasks/:id

Delete a task permanently.

**Path Parameters**:
- `id`: Task UUID

**Response** (204 No Content): Empty response body

**Errors**:
- `400`: Invalid UUID format
- `404`: Task not found

---

## Level 2 - Organization Endpoints

### GET /api/v1/tasks/tags

Retrieve all unique tags used across tasks.

**Response** (200 OK):
```json
{
  "tags": ["string"]
}
```

---

### GET /api/v1/tasks/search

Advanced search with full query parameter support (alias for GET /tasks with search-optimized response).

**Query Parameters**: Same as GET /api/v1/tasks

**Response** (200 OK): Same as GET /api/v1/tasks

---

## Level 3 - Intelligent Features Endpoints

### POST /api/v1/tasks/:id/complete

Mark a task as complete. If recurring, generate next occurrence.

**Path Parameters**:
- `id`: Task UUID

**Request Body**:
```json
{
  "completedAt": "ISO-8601 (optional, defaults to current timestamp)"
}
```

**Response** (200 OK):
```json
{
  "completed": {
    "id": "uuid",
    "completed": true,
    "updatedAt": "ISO-8601"
  },
  "nextOccurrence": {
    "id": "uuid",
    "title": "string",
    "dueDate": "ISO-8601",
    "recurrence": "daily | weekly | monthly",
    "createdAt": "ISO-8601"
  } | null
}
```

**Errors**:
- `400`: Invalid UUID format
- `404`: Task not found

---

### GET /api/v1/tasks/overdue

Retrieve all overdue tasks (dueDate < current time AND completed = false).

**Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": "uuid",
      "title": "string",
      "dueDate": "ISO-8601",
      "overdueDuration": "PT2H30M (ISO-8601 duration)"
    }
  ]
}
```

---

### GET /api/v1/tasks/reminders

Retrieve all tasks with pending reminders (reminderTime <= current time + threshold).

**Query Parameters**:
- `threshold` (optional): Lookahead duration in minutes (default: 60)

**Response** (200 OK):
```json
{
  "reminders": [
    {
      "taskId": "uuid",
      "taskTitle": "string",
      "reminderTime": "ISO-8601",
      "dueDate": "ISO-8601"
    }
  ]
}
```

---

## Validation Rules

### Title
- Required for POST, PUT
- 1-200 characters
- Must not be empty or whitespace-only

### Description
- Optional
- Max 2000 characters

### Priority
- Must be one of: `high`, `medium`, `low`
- Defaults to `medium` if not specified

### Tags
- Array of strings
- Max 10 tags per task
- Each tag max 50 characters
- Duplicates automatically removed

### Due Date
- ISO-8601 format with timezone
- Stored as UTC in database
- For new tasks, must not be more than 1 year in the future

### Recurrence
- Must be one of: `none`, `daily`, `weekly`, `monthly`
- If not `none`, dueDate is required

### Reminder Time
- Must be before dueDate
- Stored as separate field (not in main task schema for Phase 2 simplicity)

---

## Idempotency

- **GET, DELETE**: Naturally idempotent
- **PUT**: Replacing entire resource multiple times with same payload has same effect
- **POST**: Not idempotent; creates new resource each time (future: idempotency keys)
- **PATCH**: Idempotent if applied multiple times with same payload

---

## Rate Limiting

- **Phase 2**: No rate limiting enforced
- **Future**: 100 requests per minute per session (to be implemented in Phase 3)

---

## Authentication / Authorization

- **Phase 2**: No authentication required (single-user system)
- **Future**: JWT-based authentication with session management (Phase 3)

---

## Observability

All endpoints log:
- Request ID (generated per request)
- HTTP method and path
- Request timestamp
- Response status code
- Response time (milliseconds)
- Error details (if status >= 400)

Logs are structured JSON written to stdout for centralized collection.
