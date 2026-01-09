# ADR-004: API Design and Versioning Strategy

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "API Design" includes versioning, data fetching, reminder triggering, RESTful patterns).

- **Status:** Accepted
- **Date:** 2026-01-09
- **Feature:** 004-phase2-fullstack-web
- **Context:** Need comprehensive API design strategy for full-stack web application that supports frontend-backend separation, future breaking changes without disrupting clients, intelligent features (reminders with acceptable latency), and progressive enhancement (SSR for initial load, client-side fetching for interactions). Must balance simplicity (Phase 2 single-user, no real-time requirements) with extensibility (future multi-user, WebSockets, caching).

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - API design affects all client integrations and future evolution
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Multiple versioning, data fetching, and reminder strategies evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Affects frontend, backend, API contracts, deployment, caching, observability
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**API Versioning**: URL Path Versioning (`/api/v1/`, `/api/v2/`)
- **Format**: `/api/v{MAJOR}/` (e.g., `/api/v1/tasks`, `/api/v2/tasks`)
- **Version Increment Rules** (Semantic Versioning):
  - MAJOR (v1 → v2): Breaking changes (field removal, type change, endpoint removal, changed behavior)
  - MINOR (v1 → v1.1): Additive changes (new optional fields, new endpoints, new query params)
  - PATCH (v1 → v1.0.1): Non-breaking fixes (bug fixes, clarifications, no schema changes)
- **Backward Compatibility**: v1 API supported for 6 months after v2 release with deprecation headers (`X-API-Deprecated: true; sunset=2026-07-01`)

**Data Fetching Strategy**: SSR for Initial Page Load + Client-Side Fetching for Interactions
- **Initial Load**: Server-Side Rendering (SSR) in Next.js server components (fetch tasks from API, render HTML on server)
- **Interactions**: Client-side fetching for filters, search, pagination, mutations (no full page refresh)
- **Revalidation**: `router.refresh()` after mutations to refetch server data
- **Performance Target**: Initial page load < 2 seconds p95

**Reminder Triggering**: Frontend Polling (60-Second Interval)
- **Implementation**: Frontend polls `GET /api/v1/tasks/reminders` every 60 seconds
- **Response**: Backend returns tasks with `reminder_time <= current_time < due_date` (Reminder Evaluation Agent determines ready reminders)
- **Notification**: Browser notification (requires user permission) or in-app banner
- **Latency**: Max 60-second delay acceptable for task management use case (not mission-critical)
- **Simplicity**: No backend scheduler (Celery, APScheduler), no WebSockets, no persistent connections

**RESTful API Patterns**:
- **Endpoints**: 11 RESTful endpoints following HTTP semantics (GET for queries, POST for creation, PATCH for partial update, DELETE for removal)
- **Response Codes**: Standard HTTP status codes (200 OK, 201 Created, 204 No Content, 400 Bad Request, 404 Not Found, 422 Validation Error, 500 Server Error)
- **Request/Response Format**: JSON with Pydantic validation (backend) and TypeScript types (frontend)
- **Error Responses**: Structured format `{"error": {"code": "VALIDATION_ERROR", "message": "...", "details": {...}}}`
- **Pagination**: Query params `limit` (default 50) and `offset` for large result sets

**Cross-Origin Resource Sharing (CORS)**:
- **Development**: Allow `http://localhost:3000`, `http://127.0.0.1:3000` (frontend dev server)
- **Production**: Restrict to deployed frontend domain (environment-specific configuration)

## Consequences

### Positive

1. **Clear Versioning and Migration Path**:
   - URL path versioning is visible and easy to understand (version in URL)
   - Clients can migrate gradually (old clients use `/api/v1/`, new clients use `/api/v2/`)
   - 6-month backward compatibility window provides safe migration timeline
   - Deprecation headers warn clients before sunset (`X-API-Deprecated: true`)

2. **Fast Initial Page Load with SSR**:
   - User sees task list immediately (no loading spinner on first visit)
   - SSR renders HTML on server with task data (perceived performance < 2s)
   - SEO-friendly (search engines can crawl task list page, though not priority for Phase 2)
   - Better user experience than client-side-only rendering (no blank page while JS loads)

3. **Interactive UI with Client-Side Fetching**:
   - Filters, search, pagination update without full page refresh (modern web app UX)
   - Optimistic UI updates for mutations (mark complete immediately, rollback on error)
   - Lower server load (only initial SSR, subsequent interactions are client-side)

4. **Simplicity of Polling for Reminders**:
   - No additional infrastructure (no Redis, no Celery workers, no WebSocket server)
   - Stateless backend (each poll is independent query, no session tracking)
   - Acceptable latency (< 60s delay for reminder notifications)
   - Easy to test (no background worker coordination)

5. **Standard RESTful Patterns**:
   - Familiar HTTP semantics (GET, POST, PATCH, DELETE)
   - Cacheable responses (GET requests can be cached by CDN/proxy)
   - OpenAPI schema auto-generated by FastAPI (Swagger UI at `/docs`)
   - TypeScript types match Pydantic models (end-to-end type safety)

### Negative

1. **Maintenance Burden of Multiple Versions**:
   - Supporting v1 and v2 simultaneously requires maintaining parallel code paths
   - 6-month transition period means 2 versions in production (testing overhead)
   - Deprecation enforcement requires monitoring and client communication

2. **SSR Adds Network Hop**:
   - Next.js server must call FastAPI backend (server-to-server HTTP request)
   - Additional latency (~10-50ms if co-located, ~100-200ms if cross-region)
   - Tradeoff: User experience (fast initial load) outweighs server-side latency

3. **Polling Overhead and Reliability**:
   - 60-second polling adds constant load (100 concurrent users = 100 req/min)
   - Polling is less reliable than push (depends on user being online and having tab open)
   - Max 60-second delay for reminders (missed notifications if user closes tab)
   - No notifications when user is offline (acceptable for Phase 2, problematic for mission-critical)

4. **No Real-Time Updates**:
   - Task list doesn't update in real-time when data changes externally (must refresh manually or rely on polling)
   - Collaborative editing not supported (future: add WebSockets or Server-Sent Events for real-time)
   - Stale data possible if user keeps page open without refreshing

5. **Version Sprawl Risk**:
   - If API versions proliferate (v1, v2, v3, v4), maintenance becomes unsustainable
   - Mitigation: Enforce sunset policy (only 2 versions in production at any time)
   - Future: API gateway for version routing and automatic sunset enforcement

## Alternatives Considered

### Alternative A: Header Versioning + Full CSR + Backend Scheduler
- **Versioning**: `Accept: application/vnd.api.v1+json` header
- **Data Fetching**: Client-Side Rendering only (no SSR)
- **Reminders**: Backend scheduler (Celery + Redis) triggers reminders proactively

**Why Rejected**:
- Header versioning is less visible (hidden in headers, harder to test manually)
- Full CSR has slower initial load (blank page until JS loads, poor UX)
- Backend scheduler is over-engineered for Phase 2 (adds Redis, Celery workers, operational complexity)

### Alternative B: Query Parameter Versioning + ISR + WebSockets
- **Versioning**: `/api/tasks?version=1` query parameter
- **Data Fetching**: Incremental Static Regeneration (ISR, pre-render with periodic revalidation)
- **Reminders**: WebSockets for real-time push notifications

**Why Rejected**:
- Query parameter versioning is unconventional (easy to omit accidentally)
- ISR is unsuitable for dynamic data (task list changes every time user creates/completes task)
- WebSockets add complexity (persistent connections, scalability concerns, deployment overhead)

### Alternative C: No Versioning + Full SSR + Server-Sent Events
- **Versioning**: No versioning (breaking changes with migration scripts)
- **Data Fetching**: Full Server-Side Rendering (every interaction requires page refresh)
- **Reminders**: Server-Sent Events (SSE, one-way push from server)

**Why Rejected**:
- No versioning is unacceptable for multi-client system (breaking changes disrupt all clients simultaneously)
- Full SSR with page refresh on every interaction is poor UX (modern web apps expect interactivity)
- SSE still requires persistent connections (simpler than WebSockets, but adds complexity over polling)

### Alternative D: GraphQL + Client-Side Only + Polling (Same as Chosen)
- **Versioning**: GraphQL schema evolution (no versioning, clients request only needed fields)
- **Data Fetching**: Client-Side Rendering only
- **Reminders**: Frontend polling (same as chosen)

**Why Rejected**:
- GraphQL adds complexity (schema stitching, resolver logic, query parsing)
- GraphQL is over-engineered for simple CRUD API (11 endpoints, straightforward queries)
- REST with JSON is simpler and more familiar to development team
- Client-side-only rendering has poor initial load performance

## References

- Feature Spec: [specs/004-phase2-fullstack-web/sp.requirements.md](../../specs/004-phase2-fullstack-web/sp.requirements.md)
- API Contract Specification: [specs/004-phase2-fullstack-web/contracts/sp.api-contract.md](../../specs/004-phase2-fullstack-web/contracts/sp.api-contract.md)
- Frontend Behavior Specification: [specs/004-phase2-fullstack-web/contracts/sp.frontend-behavior.md](../../specs/004-phase2-fullstack-web/contracts/sp.frontend-behavior.md)
- Research Decisions: [specs/004-phase2-fullstack-web/sp.research.md](../../specs/004-phase2-fullstack-web/sp.research.md) (Decisions 3, 6, 7)
- Implementation Plan: [specs/004-phase2-fullstack-web/sp.plan.md](../../specs/004-phase2-fullstack-web/sp.plan.md)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (API & Contract Rules)
- Related ADRs: ADR-001 (Technology Stack - Next.js SSR, FastAPI REST), ADR-003 (AI-Native Architecture - Reminder Evaluation Agent)
- Evaluator Evidence: N/A (architectural decision documented in planning phase)
