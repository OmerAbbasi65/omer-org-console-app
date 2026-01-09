# Research & Design Decisions: Phase 2 Full-Stack Todo Web Application

**Feature**: 004-phase2-fullstack-web
**Created**: 2026-01-09
**Purpose**: Document all architectural and technical decisions with rationale, alternatives considered, and tradeoffs.

---

## Decision 1: Task ID Strategy

**Context**: Need globally unique identifiers for tasks that work across distributed systems and enable future multi-user support.

**Decision**: **UUID v4**

**Rationale**:
- Globally unique without coordination (no central ID server required)
- Standard PostgreSQL support with `uuid-ossp` extension
- Simple implementation in Python (uuid.uuid4()) and TypeScript (crypto.randomUUID())
- No ordering requirement for Phase 2 (chronological sorting can use `created_at` timestamp)

**Alternatives Considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| **ULID** (Universally Unique Lexicographically Sortable Identifier) | Sortable by creation time, slightly better index performance | Additional dependency, less standard than UUID | Ordering benefit not significant for Phase 2 scale; `created_at` timestamp provides same ordering capability with standard UUID |
| **Auto-incrementing INT** | Simplest, most compact (4-8 bytes vs 16 bytes UUID) | Not globally unique, breaks in distributed systems, exposes task count | Breaks with future multi-tenant deployment; exposes internal data (task count leakage) |
| **Snowflake ID** | Sortable, compact (64-bit), includes timestamp | Custom implementation required, clock synchronization dependency | Over-engineered for Phase 2; added complexity not justified |

**Tradeoffs**:
- **UUID v4 is non-sequential**: Slight index fragmentation in database (B-tree index performance)
- **16 bytes vs 4 bytes (INT)**: Larger storage footprint (acceptable at Phase 2 scale: 10,000 tasks × 16 bytes = 160 KB)
- **Simplicity wins**: Standard library support, no custom implementation, widely understood

**Performance Impact**: Negligible at Phase 2 scale (10,000 tasks, 100 concurrent users)

**Future Considerations**: If performance becomes issue (>1M tasks), consider ULID migration with backward compatibility layer

---

## Decision 2: Recurrence Modeling

**Context**: Support recurring tasks (daily, weekly, monthly) with automatic next occurrence generation. Two approaches: rule-based (store recurrence rule, calculate instances on-demand) vs instance generation (create new task rows on completion).

**Decision**: **Instance Generation on Completion**

**Rationale**:
- **Simpler Queries**: Each task is independent database row; no complex date arithmetic in queries
- **Easier Modifications**: User can edit/delete individual occurrences without affecting recurrence rule
- **Matches User Mental Model**: "Weekly standup" on Jan 10 and Jan 17 are distinct tasks, not calculated views
- **Better Query Performance**: `SELECT * FROM tasks WHERE completed = FALSE` is simple; no runtime date calculations

**Alternatives Considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| **Rule-Based** (store rule, calculate instances) | Less storage (one row per recurrence rule), no duplicate data | Complex queries (date arithmetic in SQL), harder to modify individual occurrences, poor query performance | Query complexity increases significantly; modifying/deleting single occurrence requires complex logic; performance degrades with large date ranges |
| **Pre-Generate Instances** (bulk create future occurrences) | All instances visible upfront | Wastes storage for far-future tasks, complex logic for "until" conditions, harder to change recurrence pattern | User sees tasks that may never be completed (future uncertainty); changing recurrence pattern requires deleting/recreating many rows |

**Storage Implications**:
- More rows: One row per occurrence (e.g., weekly task for 1 year = 52 rows)
- Storage cost: Acceptable at Phase 2 scale (10,000 tasks × 50% recurring × 10 occurrences avg = 50,000 total rows × ~500 bytes/row = 25 MB)

**Query Complexity**:
- **Simple**: `SELECT * FROM tasks WHERE completed = FALSE AND due_date < NOW()` (overdue tasks)
- **No Date Arithmetic**: No need for `generate_series()`, `date_trunc()`, or complex recurrence calculations in SQL

**Tradeoffs**:
- **Storage vs Query Performance**: Query performance wins for user-facing application
- **Duplication**: Task title/description duplicated across occurrences (acceptable tradeoff)

**Edge Cases Handled**:
- Month-end dates (Jan 31 → Feb 28/29): Handled by Recurrence Reasoning Agent
- Leap years: Agent calculates correctly using Python datetime
- Timezone changes (DST): Store as UTC, convert in frontend

**Future Considerations**: If storage becomes issue, add soft delete with archival table for old completed recurring tasks

---

## Decision 3: Reminder Triggering

**Context**: Support time-based reminders for tasks with due dates. Two approaches: backend scheduler (Celery, APScheduler) vs frontend polling.

**Decision**: **Frontend Polling (60-Second Interval)**

**Rationale**:
- **Simplest Implementation**: No additional infrastructure (no Redis, no Celery workers, no scheduler)
- **Phase 2 Scale**: Single-user system with max 10,000 tasks; polling overhead is negligible
- **Acceptable Latency**: Max 60-second delay for reminder notifications (user is already at computer)
- **No Operational Complexity**: No background workers to monitor, restart, or debug

**Alternatives Considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| **Backend Scheduler** (Celery + Redis) | More reliable, triggers even if user offline, sub-second precision | Requires Redis infrastructure, Celery worker processes, operational complexity | Over-engineered for Phase 2; user must be online to see reminders anyway (browser notifications); added complexity not justified |
| **WebSockets** (real-time push) | Instant notifications, no polling overhead | Persistent connections (scalability concern), more complex deployment, added infrastructure | Premature optimization; Phase 2 scale doesn't require real-time push; polling is simpler |
| **Server-Sent Events** (SSE) | One-way push (simpler than WebSockets), instant notifications | Persistent connections, more complex than polling | Still requires persistent connections; polling is simpler for Phase 2 |

**Reliability vs Simplicity Tradeoff**:
- **Reliability**: Polling is less reliable (depends on user being online and having tab open)
- **Simplicity**: Wins for Phase 2; single-user system with manual task management
- **Acceptable**: Reminder delay of < 60 seconds is acceptable for task management use case (not mission-critical notifications)

**Implementation Details**:
- Frontend polls `GET /api/v1/tasks/reminders` every 60 seconds
- Backend returns tasks with `reminder_time <= current_time < due_date`
- Frontend shows browser notification (requires user permission) or in-app banner
- No server-side state: Each poll is stateless query

**Performance Impact**: 60-second polling × 100 concurrent users = 100 req/min (negligible load)

**Future Migration Path**: Phase 3 can add backend scheduler without breaking API contract; frontend continues to poll, but backend proactively pushes notifications via WebSocket/SSE

---

## Decision 4: Agent Boundaries

**Context**: Implement reusable intelligence for task management. Two approaches: centralized "SmartTaskAgent" vs distributed subagents with clear domain boundaries.

**Decision**: **Distributed Subagents with Clear Domain Boundaries**

**Rationale**:
- **Reusability**: Each subagent can be invoked independently by different features/layers
- **Testability**: Isolated reasoning logic; easy to unit test each agent's decision-making
- **Extensibility**: Add new agents without modifying existing agents (Open/Closed Principle)
- **Constitutional Compliance**: AI-Native Architecture requires "behaviors delegated to subagents"

**Subagent Definitions** (4 total):

1. **Task-Planning Agent**:
   - **Domain**: Task dependencies, ordering, priority conflicts
   - **Inputs**: List of tasks with priorities, due dates, dependencies
   - **Outputs**: Sorted task list with reasoning, conflict detection, deadline suggestions
   - **Reusability**: Frontend (task organization UI), CLI (future), agent composition

2. **Recurrence Reasoning Agent**:
   - **Domain**: Date arithmetic, recurrence pattern calculation, edge case handling
   - **Inputs**: Task with recurrence pattern, completion time, timezone
   - **Outputs**: Next occurrence due date with calculation method and edge case handling
   - **Reusability**: Backend (complete endpoint), reminder service, frontend (preview)

3. **Reminder Evaluation Agent**:
   - **Domain**: Reminder scheduling, notification timing, missed reminder handling
   - **Inputs**: Tasks with due dates and reminder offsets, current time, user timezone
   - **Outputs**: Ready reminders with urgency and notification method
   - **Reusability**: Backend (reminders endpoint), frontend (polling service), future push service

4. **Query Interpretation Agent**:
   - **Domain**: Natural language query parsing, intent recognition, API parameter generation
   - **Inputs**: User query string, available tags, current date
   - **Outputs**: API parameters (filters, sorting, date ranges) with confidence and alternatives
   - **Reusability**: Backend (search endpoint), frontend (smart search UI), voice interface (future)

**Alternatives Considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| **Centralized "SmartTaskAgent"** | Single entry point, simpler invocation | Monolithic logic, harder to test, difficult to reuse specific capabilities | Violates Single Responsibility Principle; testing is harder (can't isolate recurrence logic from reminder logic); reusability is limited |
| **No Agents** (hardcoded logic) | Simplest, no agent framework needed | Logic buried in code, not inspectable, not reusable, violates constitutional requirement | Violates AI-Native Architecture principle; logic is not reusable across platforms (CLI, web UI, mobile) |
| **Agent Skills Only** (no subagents) | Skills are versioned and portable | Skills are passive (no autonomous reasoning), must be orchestrated by code | Skills are building blocks; subagents provide orchestration and reasoning; both are needed |

**Reusability vs Specialization Tradeoff**:
- **Specialization wins**: Each agent owns a distinct domain (no overlapping authority)
- **Reusability achieved**: Each agent is invoked by multiple features/layers (constitutional requirement met)

**Implementation**:
- Python modules in `backend/src/agents/` (e.g., `task_planning_agent.py`)
- JSON input/output contracts (Pydantic models for validation)
- Logged invocations for observability (structured JSON to stdout)

**Future Considerations**: Agent marketplace for community-created agents; agent composition (agents invoking other agents)

---

## Decision 5: Soft Delete Strategy

**Context**: Handle task deletion. Two approaches: flag-based soft delete (`deleted_at` timestamp) vs hard delete (permanent removal).

**Decision**: **Hard Delete for Phase 2** (No Soft Delete)

**Rationale**:
- **Simplicity**: No `deleted_at` field; no filtering in queries (`WHERE deleted_at IS NULL`)
- **Phase 2 is Single-User**: No compliance requirements (GDPR "right to erasure" not applicable)
- **Confirmation Prompt**: UI shows confirmation dialog before deletion; accidental deletion is rare
- **Storage Efficiency**: No accumulation of soft-deleted tasks over time

**Alternatives Considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| **Flag-Based Soft Delete** (`deleted_at` timestamp) | Undo delete, audit trail, compliance-friendly | All queries must filter `WHERE deleted_at IS NULL`, query performance impact, storage accumulation | Premature optimization; Phase 2 doesn't need audit trail or undo; query complexity not justified |
| **Archival Table** (`tasks_archived`) | No query performance impact, clear separation | Complex migration logic, cross-table queries for history, more tables to manage | Over-engineered for Phase 2; archival table adds complexity without clear benefit |

**Query Performance vs Auditability Tradeoff**:
- **Query Performance wins**: Phase 2 prioritizes fast queries over audit trail
- **Acceptable Risk**: Single-user system with confirmation prompts; accidental deletion is rare

**User Impact**:
- **No Undo**: User cannot recover deleted tasks (acceptable for Phase 2)
- **Confirmation Required**: UI must prompt "Are you sure you want to delete 'Task Title'?" before DELETE API call

**Future Migration Path**:
- Phase 3 can add `deleted_at` field (MINOR version bump, backward compatible)
- Existing hard-deleted tasks are already gone (acceptable data loss for upgrade)
- Migration script: `ALTER TABLE tasks ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE NULL`
- All queries updated: `WHERE deleted_at IS NULL`
- UI adds "Restore from Trash" feature

**Constitutional Compliance**: Hard delete does not violate constitution (soft delete is "Future Consideration" noted in data-model.md)

---

## Decision 6: Next.js Data Fetching Strategy

**Context**: Next.js supports multiple data fetching patterns: SSR (Server-Side Rendering), CSR (Client-Side Rendering), ISR (Incremental Static Regeneration), SSG (Static Site Generation).

**Decision**: **SSR for Initial Page Load + Client-Side Fetching for Interactions**

**Rationale**:
- **Fast Initial Load**: SSR renders HTML on server with task data; user sees content immediately (no loading spinner on first visit)
- **SEO-Friendly**: Search engines can crawl task list page (though SEO is not priority for Phase 2)
- **Perceived Performance**: User sees content < 2 seconds (SSR + streaming)
- **Interactivity for Filters/Search**: Client-side fetching for filters, search, pagination (no full page refresh)

**Data Fetching Patterns by Page**:

| Page | Initial Load | Interactions | Rationale |
|------|--------------|--------------|-----------|
| Home (`/`) | SSR (fetch tasks from API in server component) | Client-side (filter, search, pagination) | Fast initial render; interactive filters without page refresh |
| Task Detail (`/tasks/[id]`) | SSR (fetch single task in server component) | Client-side (edit, delete actions) | Task data available immediately; actions are client-side |
| Modals (Create/Edit) | N/A (modal state, not page) | Client-side (form submission) | Forms are client-side only |

**Alternatives Considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| **Full CSR** (Client-Side Rendering only) | Simpler (no server components), dynamic by default | Slower initial load (blank page until JS loads), SEO issues, poor perceived performance | User sees loading spinner on first visit (bad UX); initial load > 3 seconds |
| **ISR** (Incremental Static Regeneration) | Fast (pre-rendered), scalable (CDN cacheable) | Task list is dynamic (changes frequently), stale data problem, over-engineered | Task data changes every time user creates/completes task; ISR not suitable for dynamic data |
| **Full SSR** (no client-side fetching) | Simplest (all server-rendered), no client state | Every interaction requires full page refresh (poor UX), higher server load | Filter/search with full page refresh is jarring UX; modern web apps expect interactivity |

**Tradeoffs**:
- **SSR requires backend API calls from Next.js server**: Additional network hop (Next.js server → FastAPI backend)
- **Acceptable**: Next.js and FastAPI can be co-located (same region); latency < 10ms
- **Benefit outweighs cost**: User experience (fast initial load) is more important than server-side latency

**Implementation Details**:
- **Server Components**: Use `fetch()` in server components with `cache: 'no-store'` (always fresh data)
- **Client Components**: Use `fetch()` or `useSWR` for client-side data fetching with caching
- **Revalidation**: Call `router.refresh()` after mutations (create, update, delete) to refetch server data

**Performance Impact**: SSR adds ~100-200ms server processing time, but user sees content immediately (perceived performance is better)

**Future Considerations**: Add React Query or SWR for advanced client-side caching and optimistic updates

---

## Decision 7: API Versioning Strategy

**Context**: Need versioning strategy for API to support breaking changes without disrupting existing clients (frontend, CLI, future mobile apps).

**Decision**: **URL Path Versioning** (`/api/v1/`, `/api/v2/`)

**Rationale**:
- **Simple**: Version is visible in URL; easy to understand and test
- **Cacheable**: CDNs and proxies can cache different API versions independently
- **Standard REST Practice**: Widely adopted (GitHub API, Stripe API, Twilio API)
- **Clear Migration Path**: Old clients continue using `/api/v1/`, new clients use `/api/v2/`

**Versioning Format**: `/api/v{MAJOR}/` (e.g., `/api/v1/`, `/api/v2/`)

**Version Increment Rules** (Semantic Versioning):
- **MAJOR** (v1 → v2): Breaking changes (field removal, type change, endpoint removal, changed behavior)
- **MINOR** (v1 → v1.1): Additive changes (new optional fields, new endpoints, new query params)
- **PATCH** (v1 → v1.0.1): Non-breaking fixes (bug fixes, clarifications, no schema changes)

**Backward Compatibility Policy** (from constitution):
- v1 API supported for **6 months** after v2 release
- Deprecation headers added 3 months before sunset: `X-API-Deprecated: true; sunset=2026-07-01`
- Clients must migrate to v2 before sunset date

**Alternatives Considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| **Header Versioning** (`Accept: application/vnd.api.v1+json`) | URL is clean (no version in path), more "RESTful" | Less visible (hidden in headers), harder to test manually (must set header in curl/Postman), not cacheable by default | Invisible versioning makes debugging harder; manual testing requires header manipulation; caching is complex |
| **Query Parameter** (`/api/tasks?version=1`) | Flexible (can mix versions in same request) | Pollutes query namespace, easy to forget, not standard practice | Version as query param is unconventional; easy to omit accidentally |
| **No Versioning** (breaking changes with migration scripts) | Simplest (no version management) | Breaking changes disrupt all clients simultaneously, risky deployments | Unacceptable for multi-client system (web UI, CLI, future mobile); breaking changes would break all clients at once |

**Implementation Details**:
- **FastAPI Router**: Separate routers for each version (`v1_router`, `v2_router`)
- **Shared Logic**: Common services and models can be reused across versions (only API layer changes)
- **OpenAPI Schema**: Generate separate schemas for each version (`/api/v1/docs`, `/api/v2/docs`)

**Example Breaking Change Migration** (v1 → v2):

| Change | v1 Behavior | v2 Behavior | Migration Path |
|--------|-------------|-------------|----------------|
| Rename `completed` to `status` | `completed: boolean` | `status: "active" | "completed"` | v1 continues to work for 6 months; v2 uses new field; deprecation notice in v1 responses |
| Remove `description` field | `description: string` | Field removed | v2 requires clients to migrate to new `notes` field; v1 deprecated with sunset date |

**Tradeoffs**:
- **Maintenance Burden**: Supporting multiple versions requires maintaining parallel code paths (acceptable for 6-month transition period)
- **Clear Migration**: Clients have 6 months to migrate (reasonable transition period)

**Future Considerations**: If API versions proliferate (v1, v2, v3), consider API gateway for version routing and sunset enforcement

---

## Summary of Decisions

| Decision | Choice | Primary Rationale |
|----------|--------|-------------------|
| Task ID Strategy | UUID v4 | Simplicity, standard library support, globally unique |
| Recurrence Modeling | Instance Generation | Simpler queries, better query performance, matches user mental model |
| Reminder Triggering | Frontend Polling | Simplest implementation, no additional infrastructure, acceptable latency |
| Agent Boundaries | Distributed Subagents | Reusability, testability, extensibility, constitutional compliance |
| Soft Delete Strategy | Hard Delete (Phase 2) | Simplicity, no query complexity, no compliance requirements |
| Next.js Data Fetching | SSR + Client-Side | Fast initial load, interactive filters without page refresh |
| API Versioning | URL Path Versioning | Simple, visible, cacheable, standard REST practice |

---

## Implementation Impact

All decisions documented above inform:
- **Data Model**: UUID primary key, instance generation for recurrence, no soft delete field
- **API Contract**: URL path versioning (`/api/v1/`), reminder endpoint for polling
- **Frontend Behavior**: SSR for initial load, client-side fetching for interactions
- **Reusable Intelligence**: 4 distributed subagents with clear domain boundaries
- **Testing Strategy**: Test each agent in isolation, validate recurrence calculations, test API versioning

**No Unresolved Questions**: All "NEEDS CLARIFICATION" items from Technical Context have been resolved.

**Ready for Implementation**: Proceed to `/sp.tasks` to generate executable task list.
