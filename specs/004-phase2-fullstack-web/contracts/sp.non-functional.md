# Non-Functional Requirements: Phase 2 Todo Web Application

**Feature**: 004-phase2-fullstack-web
**Created**: 2026-01-09
**Purpose**: Define performance, reliability, extensibility, security, and observability requirements for the full-stack todo web application.

## Performance Expectations

### Latency Requirements

| Operation                | Target Latency (p95) | Target Latency (p99) | Justification                                    |
|--------------------------|----------------------|----------------------|--------------------------------------------------|
| Page load (initial)      | < 2 seconds          | < 3 seconds          | First Contentful Paint for acceptable UX         |
| API request (CRUD)       | < 500ms              | < 1 second           | Standard web app responsiveness                  |
| Task list rendering      | < 1 second           | < 2 seconds          | Up to 1000 tasks with filters applied            |
| Filter/search response   | < 500ms              | < 1 second           | Interactive search experience                    |
| Task creation           | < 500ms              | < 1 second           | Immediate user feedback                          |
| Recurring instance gen  | < 1 minute           | < 2 minutes          | Background process, not user-blocking            |
| Database query          | < 200ms              | < 500ms              | Single-region Neon deployment                    |

### Throughput Requirements

| Metric                      | Target Value         | Justification                                    |
|-----------------------------|----------------------|--------------------------------------------------|
| Concurrent users            | 100 users            | Phase 2 target for single-tenant deployment      |
| Requests per second (total) | 500 req/s            | ~5 req/s per user (polling, interactions)        |
| Task writes per second      | 50 writes/s          | Assumes 1 write per user every 2 seconds (peak)  |
| Database connections (max)  | 10 connections       | Neon auto-scales; 10 is sufficient for Phase 2   |

### Resource Constraints

| Resource                | Limit                | Justification                                    |
|-------------------------|----------------------|--------------------------------------------------|
| Backend memory          | < 512 MB             | Serverless backend; must fit in standard container|
| Frontend bundle size    | < 500 KB (gzipped)   | Fast initial load on slow connections            |
| Database storage        | < 10 GB              | 10,000 tasks ~1 MB; 10 GB allows 100x headroom   |
| Task payload size (max) | < 10 KB per task     | Title (200) + description (2000) + metadata      |
| API response size (max) | < 1 MB per response  | Paginated task list (50 tasks ~500 KB)           |

### Scalability Targets

| Metric                      | Phase 2 Target       | Phase 3 Target (Future)                          |
|-----------------------------|----------------------|--------------------------------------------------|
| Tasks per user              | 10,000 tasks         | 100,000 tasks                                    |
| Concurrent users            | 100 users            | 1,000 users                                      |
| Database size               | 10 GB                | 100 GB                                           |
| Requests per second         | 500 req/s            | 5,000 req/s                                      |

**Phase 2 Strategy**: Vertical scaling (increase Neon compute units, optimize queries)
**Phase 3 Strategy**: Horizontal scaling (multi-region deployment, read replicas, caching layer)

---

## Reliability Expectations

### Availability

| Service                 | Target Availability  | Downtime Allowance (per month) | Justification                |
|-------------------------|----------------------|--------------------------------|------------------------------|
| Web UI                  | 99.5%                | ~3.6 hours                     | Shared hosting acceptable    |
| Backend API             | 99.5%                | ~3.6 hours                     | Neon + FastAPI uptime        |
| Database (Neon)         | 99.9%                | ~43 minutes                    | Neon SLA guarantee           |

**Monitoring**: Track uptime via synthetic monitors (ping every 5 minutes)

### Error Budget

- **Monthly Error Budget**: 0.5% of requests can fail (e.g., 5 failures per 1000 requests)
- **Error Types Included**: 5xx server errors, network timeouts, database unavailability
- **Error Types Excluded**: 4xx client errors (user input errors, not system failures)

**Error Budget Policy**:
- If error budget is exhausted, freeze new feature development and focus on reliability improvements
- Track error budget weekly; alert if > 50% consumed before month-end

### Data Durability

- **Neon PostgreSQL**: 99.99% durability (replicated storage, automatic backups)
- **Backup Frequency**: Daily automated backups retained for 7 days (Neon default)
- **Point-in-Time Recovery**: Not implemented in Phase 2 (future: Neon PITR feature)

**Data Loss Tolerance**: Zero tolerance for data loss during normal operations (atomic transactions, rollback on failure)

### Failure Modes and Graceful Degradation

| Failure Scenario                | System Behavior                                                                 | Recovery Time Objective (RTO) |
|---------------------------------|---------------------------------------------------------------------------------|-------------------------------|
| Database connection lost        | Retry connection up to 3 times; display error banner if all retries fail       | < 30 seconds                  |
| Backend API unavailable         | Frontend shows "Service temporarily unavailable. Try again later."              | < 5 minutes (manual restart)  |
| Neon database outage            | Backend returns 503 Service Unavailable; no data mutations until DB recovers    | < 15 minutes (Neon SLA)       |
| Reminder polling failure        | Reminders delayed until next successful poll (max 60 seconds delay)             | < 1 minute                    |
| Recurring instance gen failure  | Original task remains completed; retry instance generation on next poll         | < 5 minutes (retry mechanism) |
| Frontend build failure          | Serve cached version; display warning banner                                    | < 10 minutes (rollback deploy)|

**Graceful Degradation Strategy**:
- Prioritize read operations over write operations during partial outages
- Display cached task list if backend is unreachable (stale data acceptable for 5 minutes)
- Disable features gracefully (e.g., if reminder service down, hide reminder UI)

---

## Extensibility Rules

### API Versioning

- **Current Version**: v1 (`/api/v1/...`)
- **Versioning Strategy**: URL path versioning (e.g., `/api/v2/...` for breaking changes)
- **Backward Compatibility Window**: v1 API supported for 6 months after v2 release
- **Deprecation Process**:
  1. Announce deprecation 3 months in advance
  2. Add deprecation headers to v1 responses: `X-API-Deprecated: true; sunset=2026-07-01`
  3. Monitor v1 usage; send notifications to active users
  4. Decommission v1 after sunset date

### Schema Evolution

- **Additive Changes**: New optional fields allowed in MINOR version (backward compatible)
- **Breaking Changes**: Field removal, type change, constraint tightening require MAJOR version
- **Migration Strategy**:
  1. Add new field (nullable or with default)
  2. Backfill existing records
  3. Deprecate old field
  4. Remove old field in next MAJOR version

**Example**:
- v1.0.0: `priority: ENUM('high', 'medium', 'low')`
- v1.1.0: Add `priority_score: INT (nullable)` for fine-grained priority (additive, MINOR)
- v2.0.0: Remove `priority` ENUM, use only `priority_score` (breaking, MAJOR)

### Plugin/Extension Architecture

Phase 2 does NOT support plugins. Future phases may add:

- **Extension Points**: Custom task fields, custom filters, custom agents
- **Plugin API**: RESTful webhook endpoints for third-party integrations
- **Security**: Plugins run in sandboxed environment, require user approval

---

## Security Assumptions

Phase 2 is a **single-user, local deployment** with minimal security requirements. Multi-user security is out of scope.

### Authentication / Authorization

- **Phase 2**: No authentication required (single-user system, no login)
- **Assumption**: Application is deployed locally or behind existing auth layer (e.g., VPN, firewall)
- **Future (Phase 3)**: JWT-based authentication, session management, role-based access control (RBAC)

### Data Privacy

- **Sensitive Data**: Task titles and descriptions may contain personal information
- **Encryption at Rest**: Neon PostgreSQL encrypts data at rest (default, AES-256)
- **Encryption in Transit**: All API calls use HTTPS (TLS 1.3)
- **Data Retention**: No automatic data deletion in Phase 2; user manually deletes tasks

**GDPR Compliance**: Out of scope for Phase 2 (single-user, no personal data processing beyond user's own tasks)

### Input Validation

All user inputs MUST be validated to prevent injection attacks:

| Input Field       | Validation Rules                                                                 | Attack Prevention            |
|-------------------|----------------------------------------------------------------------------------|------------------------------|
| Title             | Max 200 chars, no HTML tags, trim whitespace                                     | XSS, SQL injection           |
| Description       | Max 2000 chars, allow markdown formatting (sanitized), no `<script>` tags        | XSS                          |
| Tags              | Max 10 tags, each max 50 chars, alphanumeric + hyphen/underscore only           | Injection, path traversal    |
| Due Date          | ISO-8601 format, valid datetime, not more than 10 years in future                | Overflow, logic errors       |
| Priority          | Must be one of: `high`, `medium`, `low` (ENUM validation)                        | Injection                    |
| Recurrence        | Must be one of: `none`, `daily`, `weekly`, `monthly` (ENUM validation)           | Injection                    |

**Validation Layer**: Both frontend (UX) and backend (security) validate all inputs

**SQL Injection Prevention**: Use parameterized queries (SQLModel ORM handles this automatically)

**XSS Prevention**: Sanitize all user-generated content before rendering in HTML (use React's default escaping)

### API Security

- **Rate Limiting**: Not implemented in Phase 2 (single-user, trusted environment)
- **CORS**: Allow all origins in Phase 2 (future: restrict to known frontend domains)
- **CSRF Protection**: Not required (no cookies/sessions in Phase 2)

**Future (Phase 3)**: Add rate limiting (100 req/min per user), CORS whitelist, CSRF tokens for session-based auth

---

## Observability (Logs, Errors, Tracing - Conceptual)

### Logging Requirements

All logs MUST be structured JSON written to stdout for centralized collection.

**Log Levels**:
- **DEBUG**: Detailed diagnostic information (disabled in production)
- **INFO**: General informational messages (API requests, state transitions)
- **WARN**: Potentially harmful situations (slow queries, deprecated API usage)
- **ERROR**: Error events that may allow application to continue running
- **FATAL**: Severe errors causing application shutdown

**Log Schema**:
```json
{
  "timestamp": "ISO-8601",
  "level": "DEBUG | INFO | WARN | ERROR | FATAL",
  "service": "backend | frontend",
  "requestId": "uuid (trace requests across services)",
  "userId": "string (future: user identifier)",
  "message": "string (human-readable message)",
  "context": {
    "taskId": "uuid",
    "operation": "create_task | update_task | delete_task",
    "durationMs": number,
    "statusCode": number
  },
  "error": {
    "type": "string (error class name)",
    "message": "string",
    "stackTrace": "string (sanitized for production)"
  }
}
```

**What to Log**:

| Event Type              | Log Level | Required Fields                                      |
|-------------------------|-----------|------------------------------------------------------|
| API request received    | INFO      | method, path, requestId, timestamp                   |
| API response sent       | INFO      | statusCode, durationMs, requestId                    |
| Task created            | INFO      | taskId, userId, title, priority, timestamp           |
| Task updated            | INFO      | taskId, changedFields, timestamp                     |
| Task deleted            | INFO      | taskId, timestamp                                    |
| Recurring instance gen  | INFO      | parentTaskId, newTaskId, newDueDate, timestamp       |
| Database query (slow)   | WARN      | query, durationMs (> 500ms triggers warning)         |
| API error (4xx)         | WARN      | statusCode, errorMessage, requestId                  |
| API error (5xx)         | ERROR     | statusCode, errorMessage, stackTrace, requestId      |
| Database connection lost| ERROR     | error type, retry count, timestamp                   |

**Log Retention**: 7 days in Phase 2 (centralized log aggregator like CloudWatch or Datadog for longer retention)

### Error Tracking

- **Error Aggregation**: Group similar errors by error type, message, and stack trace
- **Error Alerting**: Send alert if > 10 errors/minute or > 1% error rate
- **Error Context**: Include request ID, user ID, task ID for debugging

**Error Reporting Service**: Not implemented in Phase 2 (future: integrate Sentry or Rollbar)

### Performance Monitoring

Track key metrics:

| Metric                      | Target Value         | Alert Threshold                                  |
|-----------------------------|----------------------|--------------------------------------------------|
| API response time (p95)     | < 500ms              | Alert if > 1 second for 5 consecutive minutes    |
| Database query time (p95)   | < 200ms              | Alert if > 500ms for 5 consecutive minutes       |
| Frontend page load (p95)    | < 2 seconds          | Alert if > 3 seconds for 5 consecutive minutes   |
| Error rate                  | < 1%                 | Alert if > 5% for 5 consecutive minutes          |
| Task creation rate          | Normal: 0-10/min     | Alert if > 100/min (potential abuse or bug)      |

**Monitoring Tools**: Not implemented in Phase 2 (future: Prometheus + Grafana, or Datadog)

### Distributed Tracing

- **Request ID**: Generate UUID for each API request; propagate through all services
- **Trace Context**: Pass request ID from frontend → backend → database
- **Trace Visualization**: Not implemented in Phase 2 (future: Jaeger or Zipkin)

**Example Trace**:
```
Request ID: 550e8400-e29b-41d4-a716-446655440000
├─ Frontend: User clicks "Create Task" (10ms)
├─ Backend: POST /api/v1/tasks (450ms)
│  ├─ Validate input (5ms)
│  ├─ Database: INSERT INTO tasks (200ms)
│  └─ Generate response (5ms)
└─ Frontend: Render new task (20ms)
Total: 480ms
```

### Health Checks

Expose health check endpoints for monitoring:

- **GET /health**: Returns 200 OK if service is healthy
- **GET /health/db**: Returns 200 OK if database is reachable
- **GET /health/ready**: Returns 200 OK if service is ready to handle traffic

**Health Check Response**:
```json
{
  "status": "healthy | degraded | unhealthy",
  "checks": {
    "database": "ok | error",
    "apiVersion": "v1",
    "uptime": "ISO-8601 duration"
  },
  "timestamp": "ISO-8601"
}
```

---

## Compliance and Standards

Phase 2 does NOT implement formal compliance (single-user, non-production system). Future phases may require:

- **GDPR**: Right to erasure, data portability, consent management
- **SOC 2**: Security controls, audit logs, access reviews
- **WCAG 2.1**: Accessibility standards (Level AA)

**Phase 2 Best Practices**:
- Follow REST API conventions (HTTP methods, status codes, resource naming)
- Use semantic HTML and ARIA labels for accessibility
- Encrypt data in transit (HTTPS) and at rest (Neon default)
- Sanitize user inputs to prevent XSS and injection attacks

---

## Future Non-Functional Enhancements

Phase 3 may add:

### Performance
- **Caching Layer**: Redis for frequently accessed task lists
- **CDN**: Static asset delivery via CDN (Cloudflare, AWS CloudFront)
- **Query Optimization**: Database indexes, query plan analysis

### Reliability
- **Multi-Region Deployment**: Active-active or active-passive failover
- **Read Replicas**: Separate read and write database connections
- **Circuit Breaker Pattern**: Prevent cascading failures

### Security
- **Multi-Factor Authentication (MFA)**: TOTP or SMS-based 2FA
- **Audit Logs**: Immutable log of all data mutations for compliance
- **Role-Based Access Control (RBAC)**: Admin, user, read-only roles

### Observability
- **Real-Time Dashboards**: Grafana dashboards for metrics
- **Anomaly Detection**: Machine learning for unusual traffic patterns
- **Distributed Tracing**: Jaeger or Zipkin for request tracing
