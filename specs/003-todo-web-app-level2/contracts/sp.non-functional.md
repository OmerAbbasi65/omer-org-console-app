# Non-Functional Requirements: Level 2 (Organization)

**Phase**: Phase 2 - Level 2 (Organization Features)
**Date**: 2026-01-09

## Overview

This document defines non-functional requirements for Level 2 (Organization) features, covering performance, reliability, extensibility, security, and observability.

---

## Performance Requirements

### API Response Times

| Operation | Target (p50) | Target (p95) | Target (p99) | Measured At |
|-----------|-------------|-------------|-------------|-------------|
| GET /tasks (no filters) | < 100ms | < 200ms | < 500ms | 1,000 tasks |
| GET /tasks (with filters) | < 150ms | < 300ms | < 600ms | 1,000 tasks |
| GET /tasks (with search) | < 200ms | < 500ms | < 1s | 1,000 tasks |
| GET /tasks (composite) | < 250ms | < 600ms | < 1.5s | 1,000 tasks |
| POST /tasks | < 100ms | < 200ms | < 500ms | N/A |
| PATCH /tasks/{id} | < 100ms | < 200ms | < 500ms | N/A |
| DELETE /tasks/{id} | < 100ms | < 200ms | < 500ms | N/A |

**Composite** = search + filter (multiple) + sort

### Frontend Performance

| Metric | Target | Measured At |
|--------|--------|-------------|
| Initial page load (FCP) | < 1.5s | Cold start |
| Time to Interactive (TTI) | < 3s | Cold start |
| Task list render | < 100ms | 50 tasks |
| Task list render | < 300ms | 500 tasks |
| Filter apply | < 1s | 1,000 tasks |
| Sort apply | < 500ms | 1,000 tasks |
| Search debounce delay | 500ms | N/A |
| Tag input response | < 16ms | Real-time typing |

### Database Query Performance

| Query Type | Target | Index Used |
|------------|--------|------------|
| Filter by priority | < 50ms | `idx_tasks_priority` |
| Filter by tag (single) | < 100ms | `idx_tasks_tags` (GIN) |
| Filter by tags (multiple) | < 150ms | `idx_tasks_tags` (GIN) |
| Search (title/description) | < 200ms | Full-text (LIKE) |
| Sort by priority | < 100ms | `idx_tasks_priority` |
| Sort by created_at | < 50ms | `idx_tasks_created_at` |
| Composite filter + sort | < 300ms | Multiple indexes |

### Throughput

| Operation | Minimum Throughput |
|-----------|-------------------|
| Read operations (GET) | 100 req/sec |
| Write operations (POST/PATCH/DELETE) | 50 req/sec |
| Concurrent users | 50 users |

**Load Testing Required**:
- Simulate 50 concurrent users
- Sustained load for 5 minutes
- Measure p50, p95, p99 latencies

---

## Reliability Requirements

### Availability

**Target**: 99.5% uptime (monthly)
- **Downtime Budget**: ~3.6 hours/month
- **Planned Maintenance**: Outside business hours

**Exclusions**:
- Neon database downtime (external dependency)
- DNS failures
- User network issues

### Error Rates

**Target**: < 0.5% error rate for all API endpoints

**Error Rate Calculation**:
```
Error Rate = (5xx responses + 4xx validation errors) / Total Requests
```

**Thresholds**:
- **Warning**: Error rate > 0.5% for 5 minutes
- **Critical**: Error rate > 2% for 5 minutes

### Data Durability

**Target**: 99.999% durability (five nines)
- **Responsibility**: Neon PostgreSQL (managed service)
- **Backup Frequency**: Neon automatic backups (point-in-time recovery)

**Data Consistency**:
- **Write Consistency**: Strong consistency (synchronous writes)
- **Read Consistency**: Eventual consistency acceptable for non-critical operations

### Graceful Degradation

**Database Unavailable**:
- Return 503 Service Unavailable
- Error message: "Database temporarily unavailable. Please try again."
- Retry with exponential backoff

**Search Timeout**:
- If search takes > 2 seconds, return partial results with warning
- Message: "Search results may be incomplete"

**Filter/Sort Timeout**:
- If query takes > 2 seconds, return unfiltered results with error
- Message: "Unable to apply filters. Showing all tasks."

---

## Scalability

### Horizontal Scalability

**Backend**:
- Stateless API servers (FastAPI)
- Can scale horizontally by adding more instances
- Load balancer distributes requests (future, not Level 2)

**Database**:
- Neon auto-scales based on demand
- Connection pooling handles concurrent requests

**Frontend**:
- Static Next.js frontend
- Can be deployed to CDN (Vercel, Netlify, Cloudflare)

### Vertical Scalability

**Task Count Limits**:

| Task Count | Expected Performance | Degradation |
|------------|---------------------|-------------|
| 0 - 1,000 | Full performance | None |
| 1,000 - 5,000 | Acceptable (< 1s operations) | Minor (search slower) |
| 5,000 - 10,000 | Degraded (< 2s operations) | Noticeable (search/filter slow) |
| 10,000+ | Unsupported in Level 2 | Pagination required |

**Mitigation for Large Datasets** (Level 3+):
- Implement pagination (offset/limit or cursor-based)
- Add full-text search index (PostgreSQL `tsvector`)
- Implement caching layer (Redis)

### Concurrent Users

**Target**: 50 concurrent users without performance degradation

**Testing**:
- Load test with 50 concurrent users
- Each user performs: create task, search, filter, sort, update, delete
- Measure p95 latency for all operations

---

## Extensibility

### Schema Extensibility

**Future Fields** (Level 3+):
- `due_date` (TIMESTAMP, nullable)
- `recurrence` (VARCHAR, nullable)
- `reminder_time` (TIMESTAMP, nullable)

**Design Principles**:
- All new fields MUST be nullable
- All new fields MUST have sensible defaults
- No field removal or renaming (only deprecation)

**Migration Strategy**:
- Additive-only migrations
- Backward-compatible API changes
- Feature flags for new functionality

### API Extensibility

**Versioning**:
- Current version: `/api/v1`
- Breaking changes require new version: `/api/v2`
- Maintain v1 for at least 6 months after v2 launch

**New Endpoints**:
- Can add new endpoints without versioning
- Cannot modify existing endpoint behavior without versioning

**New Query Parameters**:
- Can add optional query parameters
- Cannot change meaning of existing parameters

### Frontend Extensibility

**Component Reusability**:
- Components MUST be modular and reusable
- Props MUST be well-typed with TypeScript
- No hardcoded business logic in components

**State Management**:
- State MUST be centralized (React Context or props)
- No global mutable state
- Easy to swap React for another framework (conceptually)

---

## Security

### Authentication and Authorization

**Level 2 Status**: No authentication (single-user mode)

**Future Requirements** (Level 3+):
- JWT-based authentication
- Session management
- Role-based access control (RBAC)

### Input Validation

**Backend Validation** (MUST enforce):
- Title: 1-200 characters, non-empty
- Description: max 1000 characters
- Priority: enum validation ("high", "medium", "low", null)
- Tags: max 20 items, max 50 chars each, trimmed, deduplicated

**Frontend Validation** (SHOULD enforce):
- Same rules as backend (for UX, not security)
- Prevent obviously invalid submissions

**Validation Order**:
1. Frontend (immediate feedback)
2. Backend (security enforcement)

### SQL Injection Prevention

**Protection Mechanisms**:
- SQLModel parameterized queries (prevents SQL injection)
- No raw SQL strings with user input
- Pydantic validation before database operations

**Unsafe Patterns** (NEVER use):
```python
# BAD: Do not use string formatting
query = f"SELECT * FROM tasks WHERE title = '{user_input}'"

# GOOD: Use SQLModel/SQLAlchemy parameterized queries
statement = select(Task).where(Task.title == user_input)
```

### Cross-Site Scripting (XSS) Prevention

**Backend**:
- No HTML rendering in API responses (JSON only)
- Escape special characters in error messages

**Frontend**:
- React automatically escapes JSX content
- Use `dangerouslySetInnerHTML` only for trusted content (never user input)

**User Input Handling**:
- Task titles, descriptions, tags: displayed as plain text
- No markdown rendering in Level 2 (deferred to future levels)

### CORS Configuration

**Allowed Origins**:
- Development: `http://localhost:3000` (Next.js dev server)
- Production: Configure specific domain (e.g., `https://todo.example.com`)

**CORS Headers**:
```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: false (no auth in Level 2)
```

### Data Privacy

**Sensitive Data**:
- Task titles and descriptions may contain personal information
- No encryption at rest in Level 2 (Neon handles database encryption)
- HTTPS required for production (TLS 1.2+)

**Data Retention**:
- Tasks retained indefinitely until user deletes them
- No automatic data deletion in Level 2

**Data Export** (Not implemented in Level 2):
- Future: Allow users to export all tasks as JSON/CSV

---

## Observability

### Logging

**Log Levels**:

| Level | Use Case | Examples |
|-------|----------|----------|
| DEBUG | Development only | SQL queries, request payloads |
| INFO | Normal operations | Request received, task created |
| WARNING | Degraded performance | Slow query (>1s), high error rate |
| ERROR | Failures | Database connection lost, validation error |
| CRITICAL | System down | Database unreachable, server crash |

**Log Format** (Structured JSON):

```json
{
  "timestamp": "2026-01-09T10:30:00.000Z",
  "level": "INFO",
  "message": "Task created",
  "context": {
    "taskId": "550e8400-e29b-41d4-a716-446655440000",
    "userId": null,
    "operation": "create_task",
    "duration_ms": 45
  }
}
```

**Logged Events**:
- Task creation, update, deletion
- Search queries (term, result count)
- Filter operations (filters applied, result count)
- API errors (status code, error message)
- Database query execution time

**Log Aggregation** (Future):
- Level 2: Log to stdout/stderr (captured by Docker/Kubernetes)
- Level 3+: Send logs to centralized system (e.g., Datadog, CloudWatch)

### Metrics

**Key Metrics to Track**:

| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | Total API requests by endpoint, status |
| `http_request_duration_seconds` | Histogram | Request latency distribution |
| `tasks_total` | Gauge | Total number of tasks in database |
| `tasks_by_priority` | Gauge | Task count by priority level |
| `tasks_by_status` | Gauge | Task count by completion status |
| `database_query_duration_seconds` | Histogram | Database query latency |
| `search_queries_total` | Counter | Total search queries |
| `filter_operations_total` | Counter | Total filter operations |

**Metrics Endpoint** (Future):
- Expose Prometheus-compatible metrics at `/metrics`
- Not implemented in Level 2 (add in Level 3+)

### Error Tracking

**Error Tracking Requirements**:
- All 5xx errors logged with stack trace
- All 422 validation errors logged with input details (sanitized)
- Frontend errors caught with error boundary

**Error Categorization**:

| Category | HTTP Status | Severity | Alert? |
|----------|-------------|----------|--------|
| Validation Error | 422 | Low | No |
| Not Found | 404 | Low | No |
| Bad Request | 400 | Low | No |
| Internal Server Error | 500 | High | Yes |
| Database Error | 503 | Critical | Yes |

**Error Monitoring** (Future):
- Integrate Sentry or similar for error tracking
- Not required in Level 2

### Tracing

**Request Tracing** (Future - Level 3+):
- Generate unique request ID for each API call
- Propagate request ID through all layers (API → Database)
- Include request ID in all logs

**Distributed Tracing** (Not required in Level 2):
- OpenTelemetry integration (Level 3+)
- Trace API request → Database query → Response

### Health Checks

**Endpoints**:

1. **Basic Health Check**:
   ```
   GET /health
   Response: {"status": "healthy"}
   ```

2. **Database Health Check** (Future):
   ```
   GET /health/db
   Response: {
     "status": "healthy",
     "database": "connected",
     "latency_ms": 5
   }
   ```

**Health Check Criteria**:
- 200 OK: Service is healthy
- 503 Service Unavailable: Service is degraded or down

**Health Check Frequency**:
- Load balancer: every 10 seconds
- Monitoring system: every 30 seconds

---

## Testing Requirements

### Unit Testing

**Coverage Target**: > 80% code coverage

**Required Unit Tests**:
- All Pydantic validators (priority, tags, title)
- All database query functions
- All API endpoint handlers (success and error cases)
- Frontend component rendering
- Frontend state management

### Integration Testing

**Required Integration Tests**:
- Full CRUD operations (create → read → update → delete)
- Search with various terms
- Filters (single and composite)
- Sorting (all fields, both orders)
- Priority and tag operations
- Error scenarios (404, 422, 500)

### End-to-End Testing

**Required E2E Tests**:
- User creates task with priority and tags
- User searches for task
- User filters by priority and tags
- User sorts tasks
- User updates priority and tags
- User deletes task

**E2E Testing Tools** (Suggested):
- Playwright or Cypress for frontend
- pytest for backend API

### Performance Testing

**Load Testing**:
- Tool: Locust, k6, or Artillery
- Scenario: 50 concurrent users, 5 minutes
- Operations: Mix of create, read, search, filter, sort, update, delete
- Success Criteria: All p95 latencies meet targets

**Database Query Analysis**:
- Use `EXPLAIN ANALYZE` for all complex queries
- Verify indexes are being used
- Optimize queries exceeding 200ms

---

## Deployment

### Environment Separation

**Environments**:
1. **Development**: Local machine (Docker Compose)
2. **Staging**: Neon database + Vercel/Netlify (optional)
3. **Production**: Neon database + CDN hosting

**Configuration Per Environment**:
- DATABASE_URL (different Neon projects)
- FRONTEND_URL (different domains)
- LOG_LEVEL (DEBUG in dev, INFO in prod)

### Database Migrations

**Migration Process**:
1. Write migration (Alembic)
2. Test migration in development
3. Test rollback in development
4. Apply to staging
5. Verify staging functionality
6. Apply to production during maintenance window

**Rollback Plan**:
- Every migration MUST have `downgrade()` function
- Test rollback before production deployment

### Monitoring Post-Deployment

**After Level 2 Deployment**:
- Monitor error rates for 24 hours
- Check API latencies (compare to baseline)
- Verify database query performance
- Watch for slow queries (> 1s)

---

## Disaster Recovery

### Backup Strategy

**Database Backups**:
- Handled by Neon (automatic point-in-time recovery)
- Retention: 7 days (Neon free tier) or 30 days (paid tier)

**Recovery Time Objective (RTO)**: < 1 hour
**Recovery Point Objective (RPO)**: < 5 minutes (Neon's guarantee)

### Data Loss Scenarios

**Scenario 1: Database Corruption**:
- Restore from Neon automatic backup
- Downtime: ~30 minutes

**Scenario 2: Accidental Data Deletion**:
- Point-in-time recovery via Neon
- Downtime: ~15 minutes

**Scenario 3: Regional Outage**:
- Neon handles regional failover automatically
- No action required

---

## Constitutional Compliance

✅ **Performance Targets**: Explicit targets for all operations
✅ **Reliability**: Availability, error rate, and durability targets defined
✅ **Extensibility**: Clear rules for adding features without breaking changes
✅ **Security**: Input validation, SQL injection prevention, XSS protection
✅ **Observability**: Logging, metrics, tracing, and health checks defined
✅ **Spec-First**: All requirements defined before implementation
