# API Contract: Todo Web Application - Level 1 REST Endpoints

**Version**: 1.0.0
**Base URL**: `/api/v1`
**Content-Type**: `application/json`
**Phase**: Phase 2 - Level 1 (Core Features)
**Date**: 2026-01-08

## Overview

This document defines the REST API contract for Level 1 (Core) features of the Todo Web Application. All endpoints follow RESTful conventions and return JSON responses.

## Common Response Formats

### Success Response
```json
{
  "success": true,
  "data": { /* resource data */ }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { /* optional additional context */ }
  }
}
```

### HTTP Status Codes

| Status Code | Meaning |
|-------------|---------|
| 200 OK | Request successful |
| 201 Created | Resource created successfully |
| 400 Bad Request | Invalid request data |
| 404 Not Found | Resource not found |
| 422 Unprocessable Entity | Validation error |
| 500 Internal Server Error | Server error |

---

## Endpoints

### 1. Create Task

**POST** `/api/v1/tasks`

Creates a new task with title and optional description.

#### Request Body

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"  // optional
}
```

**Schema Validation**:
- `title` (required, string, min: 1 char, max: 200 chars, non-empty after trim)
- `description` (optional, string, max: 1000 chars)

#### Success Response (201 Created)

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "createdAt": "2026-01-08T10:30:00.000Z",
    "updatedAt": "2026-01-08T10:30:00.000Z"
  }
}
```

#### Error Responses

**400 Bad Request** - Missing or empty title
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Task title cannot be empty",
    "details": {
      "field": "title",
      "constraint": "non-empty"
    }
  }
}
```

**422 Unprocessable Entity** - Title too long
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Task title exceeds maximum length of 200 characters",
    "details": {
      "field": "title",
      "constraint": "max-length",
      "limit": 200
    }
  }
}
```

---

### 2. Get All Tasks

**GET** `/api/v1/tasks`

Retrieves all tasks. Returns empty array if no tasks exist.

#### Query Parameters

None for Level 1. (Level 2 will add filtering, sorting, search)

#### Success Response (200 OK)

```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": false,
        "createdAt": "2026-01-08T10:30:00.000Z",
        "updatedAt": "2026-01-08T10:30:00.000Z"
      },
      {
        "id": "660e8400-e29b-41d4-a716-446655440001",
        "title": "Finish project report",
        "description": null,
        "completed": true,
        "createdAt": "2026-01-08T09:15:00.000Z",
        "updatedAt": "2026-01-08T11:45:00.000Z"
      }
    ],
    "total": 2
  }
}
```

**Empty List Response**:
```json
{
  "success": true,
  "data": {
    "tasks": [],
    "total": 0
  }
}
```

---

### 3. Get Single Task

**GET** `/api/v1/tasks/{taskId}`

Retrieves a specific task by ID.

#### Path Parameters
- `taskId` (required, string, UUID format)

#### Success Response (200 OK)

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "createdAt": "2026-01-08T10:30:00.000Z",
    "updatedAt": "2026-01-08T10:30:00.000Z"
  }
}
```

#### Error Responses

**404 Not Found** - Task doesn't exist
```json
{
  "success": false,
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task with ID 550e8400-e29b-41d4-a716-446655440000 not found",
    "details": {
      "taskId": "550e8400-e29b-41d4-a716-446655440000"
    }
  }
}
```

**400 Bad Request** - Invalid UUID format
```json
{
  "success": false,
  "error": {
    "code": "INVALID_ID_FORMAT",
    "message": "Task ID must be a valid UUID",
    "details": {
      "taskId": "invalid-id"
    }
  }
}
```

---

### 4. Update Task

**PATCH** `/api/v1/tasks/{taskId}`

Updates a task's title and/or description. Only provided fields are updated (partial update).

#### Path Parameters
- `taskId` (required, string, UUID format)

#### Request Body

```json
{
  "title": "Buy groceries and fruits",     // optional
  "description": "Milk, eggs, bread, apples"  // optional
}
```

**Schema Validation**:
- At least one field (`title` or `description`) must be provided
- `title` (optional, string, min: 1 char, max: 200 chars, non-empty after trim)
- `description` (optional, string, max: 1000 chars, can be `null` to clear)

#### Success Response (200 OK)

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries and fruits",
    "description": "Milk, eggs, bread, apples",
    "completed": false,
    "createdAt": "2026-01-08T10:30:00.000Z",
    "updatedAt": "2026-01-08T12:15:00.000Z"  // updated timestamp
  }
}
```

#### Error Responses

**404 Not Found** - Task doesn't exist
```json
{
  "success": false,
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task with ID 550e8400-e29b-41d4-a716-446655440000 not found"
  }
}
```

**400 Bad Request** - No fields provided
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "At least one field (title or description) must be provided for update"
  }
}
```

**422 Unprocessable Entity** - Empty title
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Task title cannot be empty"
  }
}
```

---

### 5. Toggle Task Completion

**PATCH** `/api/v1/tasks/{taskId}/toggle`

Toggles a task's completion status (completed ↔ incomplete).

#### Path Parameters
- `taskId` (required, string, UUID format)

#### Request Body

None required. Current completion status is toggled automatically.

**Alternative explicit format** (optional):
```json
{
  "completed": true  // or false
}
```

#### Success Response (200 OK)

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": true,  // toggled from false
    "createdAt": "2026-01-08T10:30:00.000Z",
    "updatedAt": "2026-01-08T14:20:00.000Z"  // updated timestamp
  }
}
```

#### Error Responses

**404 Not Found** - Task doesn't exist
```json
{
  "success": false,
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task with ID 550e8400-e29b-41d4-a716-446655440000 not found"
  }
}
```

---

### 6. Delete Task

**DELETE** `/api/v1/tasks/{taskId}`

Permanently deletes a task. This operation cannot be undone.

#### Path Parameters
- `taskId` (required, string, UUID format)

#### Success Response (200 OK)

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "deleted": true
  }
}
```

#### Error Responses

**404 Not Found** - Task doesn't exist (or already deleted)
```json
{
  "success": false,
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task with ID 550e8400-e29b-41d4-a716-446655440000 not found"
  }
}
```

**Note**: Attempting to delete an already-deleted task returns 404, not 200. This ensures idempotency without masking errors.

---

## Request/Response Guarantees

### Idempotency

- **GET** requests: Always idempotent
- **POST** requests: NOT idempotent (creates new resource each time)
- **PATCH** requests: Idempotent (applying same update multiple times has same effect)
- **DELETE** requests: NOT strictly idempotent (second call returns 404)

### Concurrency

- **Race Condition Handling**: Last-write-wins for updates
- **Optimistic Locking**: Not implemented in Level 1 (consider for Level 2+)
- **Atomicity**: Each operation is atomic (no partial updates)

### Data Integrity

- All timestamps stored in UTC, returned in ISO-8601 format
- Task IDs are UUID v4 (globally unique, non-sequential)
- `createdAt` is immutable after task creation
- `updatedAt` is automatically updated on any modification
- `completed` defaults to `false` for new tasks

---

## Error Code Reference

| Error Code | HTTP Status | Description |
|------------|-------------|-------------|
| `VALIDATION_ERROR` | 400, 422 | Input validation failed |
| `TASK_NOT_FOUND` | 404 | Task ID doesn't exist |
| `INVALID_ID_FORMAT` | 400 | Task ID is not a valid UUID |
| `DATABASE_ERROR` | 500 | Database operation failed |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

---

## CORS Configuration

For Level 1 development:
- **Allowed Origins**: `http://localhost:3000` (Next.js dev server)
- **Allowed Methods**: `GET, POST, PATCH, DELETE, OPTIONS`
- **Allowed Headers**: `Content-Type, Authorization`
- **Credentials**: Not required (no auth in Level 1)

---

## OpenAPI / Swagger

FastAPI automatically generates OpenAPI documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

---

## Versioning Strategy

- **Current Version**: `v1`
- **Base Path**: `/api/v1`
- **Breaking Changes**: Will increment to `v2` (maintain `v1` for backwards compatibility)
- **Non-Breaking Changes**: Can be added to `v1` without version bump

---

## Rate Limiting

Not implemented in Level 1. Consider for production deployment.

---

## Future Considerations (Level 2 & 3)

### Level 2 Additions:
- Query parameters for filtering: `?priority=high&tag=work&status=incomplete`
- Query parameters for sorting: `?sortBy=priority&order=desc`
- Search endpoint: `/api/v1/tasks/search?q=groceries`

### Level 3 Additions:
- Due dates and reminders in task schema
- Recurring task handling on completion
- Overdue task indicators

---

## Testing

### Example cURL Commands

**Create Task**:
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

**Get All Tasks**:
```bash
curl http://localhost:8000/api/v1/tasks
```

**Update Task**:
```bash
curl -X PATCH http://localhost:8000/api/v1/tasks/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries and fruits"}'
```

**Toggle Completion**:
```bash
curl -X PATCH http://localhost:8000/api/v1/tasks/550e8400-e29b-41d4-a716-446655440000/toggle
```

**Delete Task**:
```bash
curl -X DELETE http://localhost:8000/api/v1/tasks/550e8400-e29b-41d4-a716-446655440000
```

---

## Constitutional Compliance

This API contract follows the Phase 2 constitution:

✅ **Spec-First**: API designed before implementation
✅ **Frontend/Backend Together**: Contracts define both sides of communication
✅ **Progressive Maturity**: Only Level 1 features included
✅ **Technology Stack**: RESTful design suitable for FastAPI
✅ **Data Integrity**: Clear validation rules and error handling
✅ **No Silent Assumptions**: All behaviors explicitly documented
