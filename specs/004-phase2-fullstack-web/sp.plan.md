# Implementation Plan: Phase 2 Full-Stack Todo Web Application

**Branch**: `004-phase2-fullstack-web` | **Date**: 2026-01-09 | **Spec**: [sp.requirements.md](sp.requirements.md)
**Input**: Feature specification set from `/specs/004-phase2-fullstack-web/`

## Summary

Build a full-stack web application for task management using Next.js (App Router) frontend, FastAPI backend, SQLModel ORM, and Neon PostgreSQL database. The system implements three progressive feature levels (Core → Organization → Intelligent) with AI-native architecture incorporating reusable intelligence via Claude Code Subagents and Agent Skills. The implementation follows spec-driven development with explicit API contracts, data models, and state management specifications.

**Primary Requirement**: Transition from CLI-based task management to accessible web interface with progressive feature maturity.

**Technical Approach**: Full-stack separation with RESTful API contracts, server-side rendering for initial loads, and agent-assisted intelligent features (recurring tasks, reminders, task planning).

---

## Technical Context

**Language/Version**:
- **Frontend**: TypeScript 5.3+ with Next.js 14+ (App Router)
- **Backend**: Python 3.11+
- **Database**: PostgreSQL 15+ (Neon Serverless)

**Primary Dependencies**:
- **Frontend**: Next.js 14+, React 18+, TypeScript 5.3+, TailwindCSS 3+ (styling), Zod (validation)
- **Backend**: FastAPI 0.109+, SQLModel 0.0.14+, Pydantic 2.5+, Uvicorn (ASGI server), Alembic (migrations)
- **Database**: Neon PostgreSQL (serverless), psycopg3 (driver)
- **Testing**: Pytest (backend), Jest + React Testing Library (frontend), Playwright (E2E)

**Storage**:
- **Database**: Neon Serverless PostgreSQL (primary storage for tasks)
- **Session**: No persistent sessions in Phase 2 (single-user, stateless)
- **Cache**: No caching layer in Phase 2 (future: Redis)

**Testing**:
- **Backend**: pytest with pytest-asyncio for async tests
- **Frontend**: Jest for unit/integration, React Testing Library for component tests
- **E2E**: Playwright for full-stack acceptance tests
- **API**: Contract testing with OpenAPI schema validation

**Target Platform**:
- **Frontend**: Modern browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
- **Backend**: Linux server (Docker container, Python 3.11+ runtime)
- **Database**: Neon cloud infrastructure (serverless PostgreSQL)

**Project Type**: Web application (frontend + backend)

**Performance Goals**:
- API response time (p95): < 500ms
- Page load (initial, p95): < 2 seconds
- Task list rendering (1000 tasks, p95): < 1 second
- Concurrent users: 100 users
- Requests per second: 500 req/s

**Constraints**:
- Backend memory: < 512 MB (serverless container limit)
- Frontend bundle: < 500 KB gzipped (fast load on slow connections)
- Database connections: Max 10 concurrent (Neon auto-scales)
- API response size: < 1 MB per response (pagination required)
- No real-time updates in Phase 2 (polling only for reminders)

**Scale/Scope**:
- Tasks per user: 10,000 tasks (Phase 2 target)
- Database size: < 10 GB
- API endpoints: 11 RESTful endpoints
- Frontend pages: 3 pages (Home, Task Detail, modals)
- Subagents: 4 (Task-Planning, Recurrence Reasoning, Reminder Evaluation, Query Interpretation)
- Agent Skills: 4 (Task Decomposition, Priority Conflict Resolution, Smart Due Date Suggestion, Recurrence Pattern Validator)

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Constitutional Requirements (Phase 2 - v2.0.0)

| Requirement | Status | Validation |
|-------------|--------|------------|
| **Spec-First, Full-Stack** | ✅ PASS | All specs created before implementation; API contracts, data model, frontend behavior, state lifecycle documented |
| **No Code Without Spec** | ✅ PASS | No code will be written until all Phase 1 design artifacts are complete |
| **Frontend and Backend Designed Together** | ✅ PASS | API contracts defined; frontend behavior spec references API endpoints; no sequential design |
| **API Contracts Defined Before Implementation** | ✅ PASS | [sp.api-contract.md](contracts/sp.api-contract.md) complete with 11 endpoints, request/response schemas |
| **Schema Changes Specified Before Code** | ✅ PASS | [sp.data-model.md](contracts/sp.data-model.md) defines Task model with migration strategy |
| **AI-Native Architecture** | ✅ PASS | [sp.reusable-intelligence.md](contracts/sp.reusable-intelligence.md) defines 4 subagents + 4 skills |
| **Agents Reason Over Tasks** | ✅ PASS | Subagents use structured JSON inputs/outputs; logic is inspectable and reusable |
| **Behaviors Delegated to Subagents** | ✅ PASS | Task planning, recurrence reasoning, reminder evaluation, query interpretation delegated to subagents |
| **Progressive Feature Maturity (3 Levels)** | ✅ PASS | Level 1 (Core) → Level 2 (Organization) → Level 3 (Intelligent) enforced with blocking gates |
| **No Feature May Skip Levels** | ✅ PASS | Implementation plan sequences features strictly (Step 1 → Step 2 → Step 3) |
| **Each Level Must Pass Acceptance Criteria** | ✅ PASS | Acceptance scenarios defined for each user story; validation gates in place |
| **Technology Stack Compliance** | ✅ PASS | Next.js (App Router) ✓, FastAPI ✓, SQLModel ✓, Neon PostgreSQL ✓ |
| **Frontend: App Router Mandatory** | ✅ PASS | Next.js 14+ App Router (not Pages Router) specified |
| **Frontend: No Direct DB Access** | ✅ PASS | Frontend behavior spec enforces API-only data access |
| **Frontend: UI Stateless by Default** | ✅ PASS | State lives in backend or controlled stores; no implicit component state |
| **Backend: Single Source of Truth** | ✅ PASS | Backend acts as data authority; frontend consumes only via API |
| **Backend: No Business Logic in Routes** | ✅ PASS | Architecture separates routes (adapters), services (logic), domain (models) |
| **Backend: Logic in Services/Domain/Agents** | ✅ PASS | Service layer + agent-assisted layers for intelligent features |
| **Data Layer: SQLModel is Canonical Schema** | ✅ PASS | [sp.data-model.md](contracts/sp.data-model.md) uses SQLModel-style schemas |
| **Data Layer: No Schema Changes Without Migration** | ✅ PASS | Migration spec required before schema changes (Alembic workflow) |
| **Data Layer: Only Additive Changes (Backward Compatible)** | ✅ PASS | Schema evolution strategy documented; no breaking changes in MINOR versions |
| **Data Layer: IDs Globally Unique (UUID)** | ✅ PASS | Task model uses UUID v4 for primary key |
| **Data Layer: Time Fields Timezone-Aware (UTC)** | ✅ PASS | All timestamps stored as UTC, converted to local timezone in frontend |
| **Reusable Intelligence: First-Class Artifact** | ✅ PASS | Dedicated specification with subagents and skills; versioned and reusable |
| **Subagents: Clear Responsibility** | ✅ PASS | Each subagent has single, well-defined purpose (no overlapping authority) |
| **Subagents: Explicit Inputs/Outputs** | ✅ PASS | All subagents use structured JSON contracts |
| **Subagents: No Direct UI Access** | ✅ PASS | Subagents operate on data only; frontend invokes via API |
| **Subagents: No Direct DB Access (Unless Authorized)** | ✅ PASS | Subagents read data via service layer; no direct database mutations |
| **Agent Skills: Versioned (Semver)** | ✅ PASS | All skills use MAJOR.MINOR.PATCH versioning |
| **Agent Skills: Context-Independent** | ✅ PASS | Skills accept JSON input, return JSON output; no hardcoded paths or secrets |
| **Agent Skills: Reusable Across Platforms** | ✅ PASS | CLI, Web UI, mobile, future agents can all invoke skills |
| **API & Contract Rules: Documented APIs** | ✅ PASS | [sp.api-contract.md](contracts/sp.api-contract.md) documents all endpoints |
| **API & Contract Rules: Validated Schemas** | ✅ PASS | Pydantic models (backend), TypeScript types (frontend) |
| **API & Contract Rules: Structured Error Responses** | ✅ PASS | Error response schema defined with error codes, messages, details |

**Constitution Check Result**: ✅ **PASS** - All 34 constitutional requirements met

**No Complexity Violations**: No justifications required

---

## Project Structure

### Documentation (this feature)

```text
specs/004-phase2-fullstack-web/
├── sp.plan.md                    # This file (/sp.plan command output)
├── sp.requirements.md            # Main requirements (already exists)
├── sp.research.md                # Phase 0 output (to be generated)
├── sp.data-model.md              # Phase 1 output (already exists in contracts/)
├── sp.quickstart.md              # Phase 1 output (to be generated)
├── contracts/                    # Phase 1 output (already exists)
│   ├── sp.api-contract.md        # 11 RESTful endpoints (already exists)
│   ├── sp.data-model.md          # Task model, recurrence, reminder (already exists)
│   ├── sp.state-and-lifecycle.md # State transitions (already exists)
│   ├── sp.frontend-behavior.md   # Pages, data-fetching, UI rules (already exists)
│   ├── sp.reusable-intelligence.md # Subagents + skills (already exists)
│   └── sp.non-functional.md      # Performance, reliability, security (already exists)
├── checklists/
│   └── requirements.md           # Validation checklist (already exists)
└── tasks.md                      # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
todoapp/
├── backend/                      # FastAPI backend
│   ├── src/
│   │   ├── models/               # SQLModel entities (Task, etc.)
│   │   ├── services/             # Business logic (TaskService, etc.)
│   │   ├── agents/               # Subagent implementations
│   │   │   ├── task_planning_agent.py
│   │   │   ├── recurrence_reasoning_agent.py
│   │   │   ├── reminder_evaluation_agent.py
│   │   │   └── query_interpretation_agent.py
│   │   ├── api/                  # FastAPI routes/endpoints
│   │   │   ├── tasks.py          # Task CRUD endpoints
│   │   │   ├── filters.py        # Search/filter endpoints
│   │   │   └── agents.py         # Agent invocation endpoints (future)
│   │   ├── database.py           # Database connection, session management
│   │   ├── config.py             # Configuration (env vars, settings)
│   │   └── main.py               # FastAPI application entry point
│   ├── tests/
│   │   ├── unit/                 # Unit tests for services, models
│   │   ├── integration/          # Integration tests for API endpoints
│   │   └── contract/             # Contract tests (OpenAPI schema validation)
│   ├── alembic/                  # Database migrations
│   │   └── versions/             # Migration scripts
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile                # Backend container image
│
├── frontend/                     # Next.js frontend
│   ├── src/
│   │   ├── app/                  # App Router pages
│   │   │   ├── page.tsx          # Home page (task list)
│   │   │   ├── tasks/
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx  # Task detail page
│   │   │   ├── layout.tsx        # Root layout
│   │   │   └── actions/          # Server actions
│   │   ├── components/           # React components
│   │   │   ├── TaskList.tsx      # Task list component
│   │   │   ├── TaskCard.tsx      # Task card component
│   │   │   ├── TaskForm.tsx      # Task creation/edit form
│   │   │   ├── FilterBar.tsx     # Filter controls
│   │   │   └── modals/           # Modal components
│   │   ├── lib/                  # Utilities
│   │   │   ├── api.ts            # API client (fetch wrappers)
│   │   │   ├── types.ts          # TypeScript types (mirrors Pydantic models)
│   │   │   └── utils.ts          # Helper functions
│   │   └── styles/               # Global styles, TailwindCSS config
│   ├── tests/
│   │   ├── unit/                 # Unit tests (Jest)
│   │   ├── integration/          # Integration tests (React Testing Library)
│   │   └── e2e/                  # End-to-end tests (Playwright)
│   ├── package.json              # Node dependencies
│   ├── tsconfig.json             # TypeScript config
│   ├── next.config.js            # Next.js config
│   └── Dockerfile                # Frontend container image
│
├── .specify/                     # Spec-Kit Plus artifacts
│   ├── skills/                   # Agent Skills (JSON schemas)
│   │   ├── task-decomposition-v1.0.0.json
│   │   ├── priority-conflict-resolution-v1.0.0.json
│   │   ├── smart-due-date-suggestion-v1.0.0.json
│   │   └── recurrence-pattern-validator-v1.0.0.json
│   └── memory/
│       └── constitution.md       # Project constitution (v2.0.0)
│
├── docker-compose.yml            # Local development setup (backend + frontend + db)
├── .env.example                  # Environment variables template
└── README.md                     # Project overview and setup instructions
```

**Structure Decision**: **Web application structure (Option 2)** selected because:
- Feature requires distinct frontend and backend with clear API boundary
- Next.js (App Router) frontend is separate concern from FastAPI backend
- Enables parallel development of frontend and backend teams
- Supports independent testing and deployment of each layer
- Aligns with constitutional requirement for full-stack separation

---

## Complexity Tracking

No constitutional violations detected. No complexity justification required.

---

## Phase 0: Research & Decision Documentation

### Objectives

- Resolve all "NEEDS CLARIFICATION" items from Technical Context (none identified)
- Research best practices for Next.js + FastAPI + SQLModel integration
- Document technology decisions with rationale and tradeoffs

### Research Tasks

1. **Task ID Strategy (UUID vs ULID)**
   - **Decision**: UUID v4
   - **Rationale**: Globally unique, standard PostgreSQL support, no ordering requirement for Phase 2
   - **Alternatives Considered**: ULID (sortable UUIDs) - rejected because chronological ordering can use `created_at` timestamp; added complexity not justified
   - **Tradeoffs**: UUID v4 is non-sequential (slight index fragmentation), but simplicity outweighs performance cost at Phase 2 scale (10,000 tasks)

2. **Recurrence Modeling (Rule-Based vs Instance Generation)**
   - **Decision**: Instance generation on completion
   - **Rationale**: Simpler queries (each task is independent row), easier to modify/delete individual occurrences, matches user mental model
   - **Alternatives Considered**: Rule-based (store recurrence rule, calculate instances on-demand) - rejected because query complexity increases, harder to handle exceptions
   - **Storage Implications**: More rows (one per occurrence), but better query performance for common operations (list active tasks)
   - **Query Complexity**: Simple queries (`SELECT * FROM tasks WHERE completed = FALSE`), no complex date arithmetic in queries

3. **Reminder Triggering (Polling vs Scheduled Evaluation)**
   - **Decision**: Frontend polling (60-second interval)
   - **Rationale**: Simplest implementation for Phase 2; no additional infrastructure (no scheduler, no background workers)
   - **Alternatives Considered**: Backend scheduler (Celery, APScheduler) - rejected because adds operational complexity; Phase 2 scale doesn't justify
   - **Reliability vs Simplicity**: Polling is less reliable (depends on user being online), but simplicity wins for Phase 2; future: migrate to backend scheduler
   - **Tradeoff**: Max 60-second delay for reminder notifications (acceptable for Phase 2)

4. **Agent Boundaries (Centralized vs Distributed Subagents)**
   - **Decision**: Distributed subagents with clear domain boundaries
   - **Rationale**: Reusability (each subagent can be invoked independently), testability (isolate reasoning logic), extensibility (add new agents without modifying existing)
   - **Alternatives Considered**: Centralized "SmartTaskAgent" - rejected because monolithic agents are harder to test, maintain, and reuse
   - **Reusability vs Specialization**: Specialization wins for AI-native architecture; each subagent owns a distinct domain
   - **Implementation**: 4 subagents (Task-Planning, Recurrence Reasoning, Reminder Evaluation, Query Interpretation) with JSON contracts

5. **Soft Delete Strategy (Flag-Based vs Archival Table)**
   - **Decision**: Hard delete for Phase 2 (no soft delete)
   - **Rationale**: Simplicity (no deleted_at field, no filtering in queries); Phase 2 is single-user with manual confirmation
   - **Alternatives Considered**: Flag-based soft delete (`deleted_at` timestamp) - deferred to Phase 3 when multi-user or compliance requirements emerge
   - **Query Performance vs Auditability**: Query performance favored for Phase 2; auditability not required for single-user system
   - **Future Migration**: Can add `deleted_at` field in MINOR version (backward compatible); existing hard-deleted tasks are already gone (acceptable data loss for Phase 2)

6. **Next.js Data Fetching Strategy (SSR vs CSR vs ISR)**
   - **Decision**: SSR for initial page load, client-side fetching for interactions
   - **Rationale**: Fast initial load (SEO-friendly, perceived performance), interactivity for filters/search (no full page refresh)
   - **Alternatives Considered**: Full CSR (slower initial load), ISR (Incremental Static Regeneration - overkill for dynamic task list)
   - **Tradeoff**: SSR requires backend API calls from Next.js server (additional network hop), but user experience benefit outweighs

7. **API Versioning Strategy (URL Path vs Header)**
   - **Decision**: URL path versioning (`/api/v1/`, `/api/v2/`)
   - **Rationale**: Simple, visible, cacheable, standard REST practice
   - **Alternatives Considered**: Header versioning (`Accept: application/vnd.api.v1+json`) - rejected because less visible, harder to test manually
   - **Backward Compatibility**: v1 API supported for 6 months after v2 release (constitutional requirement)

### Research Artifacts

Output: [sp.research.md](sp.research.md) (to be generated with above decisions documented)

---

## Phase 1: Design & Contracts

### Objectives

- Generate data models from entities identified in requirements
- Extract API endpoints from functional requirements and user actions
- Create quickstart guide for developers

### Data Model Design

**Input**: [sp.requirements.md](sp.requirements.md) - Key Entities section
**Output**: **Already exists** - [contracts/sp.data-model.md](contracts/sp.data-model.md)

**Entities Extracted**:
1. **Task**: Primary entity with 11 fields (id, title, description, completed, priority, tags, due_date, recurrence, parent_id, created_at, updated_at)
2. **Recurrence Pattern**: Conceptual model embedded in Task (recurrence field + instance generation logic)
3. **Reminder**: Conceptual model (no separate table; calculated on-demand from due_date and reminder_offset)

**Validation Rules**: Defined in data-model.md (check constraints, indexes, relationships)

**State Transitions**: Defined in [contracts/sp.state-and-lifecycle.md](contracts/sp.state-and-lifecycle.md)

### API Contract Generation

**Input**: [sp.requirements.md](sp.requirements.md) - Functional Requirements
**Output**: **Already exists** - [contracts/sp.api-contract.md](contracts/sp.api-contract.md)

**Endpoints Extracted** (11 total):

**Level 1 - Core**:
1. `POST /api/v1/tasks` - Create task (FR-001, FR-002)
2. `GET /api/v1/tasks` - List tasks with filters (FR-003, FR-012 to FR-016)
3. `GET /api/v1/tasks/:id` - Get single task (FR-003)
4. `PUT /api/v1/tasks/:id` - Replace task (FR-005)
5. `PATCH /api/v1/tasks/:id` - Update task fields (FR-005)
6. `DELETE /api/v1/tasks/:id` - Delete task (FR-006)

**Level 2 - Organization**:
7. `GET /api/v1/tasks/tags` - Get all tags (FR-014)
8. `GET /api/v1/tasks/search` - Advanced search (FR-011)

**Level 3 - Intelligent**:
9. `POST /api/v1/tasks/:id/complete` - Complete task, generate next occurrence (FR-004, FR-019)
10. `GET /api/v1/tasks/overdue` - Get overdue tasks (FR-020)
11. `GET /api/v1/tasks/reminders` - Get pending reminders (FR-021, FR-022)

**API Patterns**: RESTful HTTP with JSON payloads, standard status codes (200, 201, 204, 400, 404, 422, 500)

### Quickstart Guide

**Output**: [sp.quickstart.md](sp.quickstart.md) (to be generated)

**Contents**:
- Prerequisites (Node.js 20+, Python 3.11+, Docker, Neon account)
- Local development setup (clone repo, install dependencies, configure .env)
- Running backend (uvicorn, database migrations)
- Running frontend (next dev)
- Running tests (pytest, jest, playwright)
- API examples (curl commands for each endpoint)
- Common development tasks (add migration, add new endpoint, add component)

---

## Phase 2: Implementation Sequencing

### Feature Rollout Plan

**Constitutional Constraint**: No step may start before the previous step is validated.

#### Step 1 - Level 1 (Core) - BLOCKING

**Features**:
- Task CRUD operations (create, read, update, delete)
- Completion status toggle (mark complete/incomplete)
- Task list view with pagination

**API Endpoints**:
- POST /api/v1/tasks
- GET /api/v1/tasks (with pagination)
- GET /api/v1/tasks/:id
- PUT /api/v1/tasks/:id
- PATCH /api/v1/tasks/:id
- DELETE /api/v1/tasks/:id

**Frontend Pages**:
- Home page (task list with Add Task button)
- Task creation modal
- Task edit modal
- Task detail page (optional for Level 1)

**Acceptance Criteria** (from User Story 1):
1. ✅ User can create task "Buy groceries" and see it in list
2. ✅ User can mark task complete and styling updates
3. ✅ Tasks persist across page refreshes
4. ✅ User can edit task title and changes are saved

**Validation Gate**: All Level 1 acceptance scenarios pass; API contract tests pass; frontend E2E tests pass

---

#### Step 2 - Level 2 (Organization) - UNLOCKED AFTER STEP 1

**Features**:
- Priority levels (High, Medium, Low)
- Tags/categories
- Search by keyword (title/description)
- Filter by status, priority, tag (composable)
- Sort by creation date, due date, priority, alphabetical

**API Endpoints**:
- GET /api/v1/tasks (with filter/search/sort query params)
- GET /api/v1/tasks/tags
- GET /api/v1/tasks/search

**Frontend Components**:
- FilterBar component (dropdowns, search input, sort selector)
- Tag input component
- Priority selector component

**Acceptance Criteria** (from User Story 2):
1. ✅ User can set priority and tags when creating task
2. ✅ User can filter by priority and see only matching tasks
3. ✅ User can filter by tag and see only matching tasks
4. ✅ User can search by keyword and see matching tasks
5. ✅ User can apply multiple filters (composable)

**Validation Gate**: All Level 2 acceptance scenarios pass; filter/search queries performant (< 500ms p95); no regressions in Level 1

---

#### Step 3 - Level 3 (Intelligent) - UNLOCKED AFTER STEP 2

**Features**:
- Due dates with timezone handling
- Recurring tasks (daily, weekly, monthly)
- Auto-generation of next occurrence on completion
- Overdue task indicators
- Reminder notifications (browser notifications preferred, in-app fallback)

**API Endpoints**:
- POST /api/v1/tasks/:id/complete (generate next occurrence)
- GET /api/v1/tasks/overdue
- GET /api/v1/tasks/reminders

**Frontend Components**:
- Due date picker (date + time)
- Recurrence selector (dropdown)
- Reminder offset input
- Overdue indicator badge
- Notification component (browser API integration)

**Backend Agents**:
- Recurrence Reasoning Agent (calculate next occurrence)
- Reminder Evaluation Agent (determine ready reminders)

**Acceptance Criteria** (from User Story 3):
1. ✅ User can set due date and it's stored as UTC
2. ✅ Completing recurring task generates next occurrence
3. ✅ Overdue tasks are visually highlighted
4. ✅ Reminder notifications appear at scheduled time
5. ✅ Deleting recurring task handles child instances

**Validation Gate**: All Level 3 acceptance scenarios pass; recurring instance generation accurate (no date calculation errors); reminders trigger within 30 seconds of scheduled time; no regressions in Level 1 or Level 2

---

### Parallel Development Opportunities

**Phase 2 allows parallel work after Level 1 is complete**:

| Team/Agent | Work Stream | Dependencies |
|------------|-------------|--------------|
| Backend Team | Level 2 API endpoints (filters, search, tags) | Level 1 API complete |
| Frontend Team | Level 2 UI components (FilterBar, priority, tags) | Level 1 UI complete |
| Agent Team | Task-Planning Agent, Query Interpretation Agent | None (can start immediately with spec) |
| Backend Team | Level 3 API endpoints (complete, overdue, reminders) | Level 2 API complete |
| Frontend Team | Level 3 UI components (due date, recurrence, reminders) | Level 2 UI complete |
| Agent Team | Recurrence Reasoning Agent, Reminder Evaluation Agent | None (can start immediately with spec) |

**Critical Path**: Level 1 → Level 2 → Level 3 (sequential, blocking gates)

**Parallelizable**: Within each level, backend API + frontend UI + agent development can proceed in parallel (after contracts are defined)

---

## Phase 3: Integration & Reusable Intelligence

### Integration Strategy

**Frontend ↔ Backend Integration**:
- Frontend consumes only documented API endpoints (no direct DB access)
- All API calls use fetch with TypeScript types matching Pydantic models
- Error handling uses structured error responses (error code, message, details)
- Optimistic UI updates for mark complete, delete (rollback on API error)

**Backend ↔ Database Integration**:
- SQLModel ORM for all database operations (no raw SQL except for complex analytics)
- Alembic for schema migrations (version-controlled, reversible)
- Connection pooling (max 10 connections, managed by SQLModel/SQLAlchemy)

**Backend ↔ Agents Integration**:
- Agents invoked via Python imports (no HTTP calls in Phase 2; future: agent API endpoints)
- Agents receive structured JSON input, return structured JSON output
- Agent errors logged but do not crash main application (graceful degradation)

### Reusable Intelligence Integration

**Agent Skills** (4 total, stored in `.specify/skills/`):
1. **task-decomposition-v1.0.0.json**: Break complex task into subtasks
2. **priority-conflict-resolution-v1.0.0.json**: Detect and resolve priority conflicts
3. **smart-due-date-suggestion-v1.0.0.json**: Suggest realistic due dates based on workload
4. **recurrence-pattern-validator-v1.0.0.json**: Validate recurrence pattern matches user intent

**Subagents** (4 total, implemented in `backend/src/agents/`):
1. **Task-Planning Agent** (`task_planning_agent.py`): Reason about dependencies, ordering, priorities
2. **Recurrence Reasoning Agent** (`recurrence_reasoning_agent.py`): Calculate next occurrence dates with edge case handling
3. **Reminder Evaluation Agent** (`reminder_evaluation_agent.py`): Determine when reminders should trigger
4. **Query Interpretation Agent** (`query_interpretation_agent.py`): Parse natural language queries into API parameters

**Reusability Requirements** (from constitution):
- Agents must be reused by at least 2 features or 2 system layers
- **Task-Planning Agent**: Used by frontend (task organization UI) + CLI (future: task planning command)
- **Recurrence Reasoning Agent**: Used by backend (complete endpoint) + reminder service (calculate reminder times)
- **Reminder Evaluation Agent**: Used by backend (reminders endpoint) + frontend (polling service)
- **Query Interpretation Agent**: Used by backend (search endpoint) + frontend (smart search UI)

**Observability**: All agent invocations logged with structured JSON (timestamp, agentName, inputSummary, outputSummary, durationMs, success)

---

## Phase 4: Testing & Validation Strategy

### Validation Sources

1. **Acceptance Criteria**: From [sp.requirements.md](sp.requirements.md) - User Scenarios section
2. **API Contracts**: From [contracts/sp.api-contract.md](contracts/sp.api-contract.md) - Request/response schemas
3. **State Rules**: From [contracts/sp.state-and-lifecycle.md](contracts/sp.state-and-lifecycle.md) - State transitions

### Testing Layers

#### 1. API Validation (Backend)

**Tool**: pytest with pytest-asyncio

**Tests**:
- **Schema Validation**: All endpoints validate request payloads against Pydantic models
- **Error Handling**: 400, 404, 422, 500 errors return structured error responses
- **Contract Compliance**: OpenAPI schema generated from FastAPI app matches [sp.api-contract.md](contracts/sp.api-contract.md)

**Example Test**:
```python
# tests/integration/test_tasks_api.py
def test_create_task_validates_title_max_length():
    response = client.post("/api/v1/tasks", json={"title": "x" * 201})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
```

#### 2. Feature Validation (Frontend + Backend)

**Tool**: Playwright (E2E), React Testing Library (component)

**Tests**:
- **Happy Paths**: User can complete primary flows (create task, mark complete, filter by priority)
- **Edge Cases**: Empty state, network errors, invalid inputs
- **Failure Modes**: API errors, concurrent edits, browser refresh

**Example Test**:
```typescript
// tests/e2e/level1-core.spec.ts
test('User can create task and see it persist after refresh', async ({ page }) => {
  await page.goto('/');
  await page.click('button:has-text("Add Task")');
  await page.fill('input[name="title"]', 'Buy groceries');
  await page.click('button:has-text("Save")');
  await expect(page.locator('text=Buy groceries')).toBeVisible();
  await page.reload();
  await expect(page.locator('text=Buy groceries')).toBeVisible();
});
```

#### 3. Agent Validation (Subagents + Skills)

**Tool**: pytest with JSON schema validation

**Tests**:
- **Deterministic Outputs**: Same input produces same output (no randomness)
- **Idempotency**: Invoking agent multiple times with same input is safe
- **Schema Adherence**: Agent outputs match JSON schema defined in spec

**Example Test**:
```python
# tests/unit/test_recurrence_reasoning_agent.py
def test_recurrence_agent_calculates_weekly_occurrence():
    input_data = {
        "task": {
            "id": "uuid-123",
            "title": "Weekly standup",
            "dueDate": "2026-01-10T10:00:00Z",
            "recurrence": "weekly",
            "completedAt": "2026-01-10T10:30:00Z"
        },
        "timezone": "UTC"
    }
    result = recurrence_reasoning_agent.calculate_next_occurrence(input_data)
    assert result["nextOccurrence"]["dueDate"] == "2026-01-17T10:00:00Z"
```

#### 4. Integration Validation (Full-Stack)

**Tool**: Playwright (E2E with API mocking)

**Tests**:
- **UI ↔ API Consistency**: Frontend displays data correctly from API responses
- **Agent-Assisted Flows**: Recurring task completion generates next occurrence (UI → API → Agent → DB → UI)

**Example Test**:
```typescript
// tests/e2e/level3-intelligent.spec.ts
test('Completing recurring task generates next occurrence', async ({ page }) => {
  // Create recurring task
  await createRecurringTask(page, 'Weekly review', 'weekly', '2026-01-10T15:00:00Z');
  // Mark complete
  await page.click('button:has-text("Complete")');
  // Verify next occurrence appears
  await expect(page.locator('text=Weekly review').nth(1)).toBeVisible();
  // Verify due date is 7 days later
  await expect(page.locator('text=Jan 17, 2026')).toBeVisible();
});
```

---

## Quality Enforcement Rules

**Constitutional Requirements**:
1. ✅ No implementation without passing validation gate
2. ✅ No feature without acceptance criteria (all user stories have acceptance scenarios)
3. ✅ No agent without a spec (all 4 subagents + 4 skills documented in [sp.reusable-intelligence.md](contracts/sp.reusable-intelligence.md))
4. ✅ No undocumented decisions (all 7 decisions documented in Phase 0 research)

**Additional Rules**:
- All API endpoints must have integration tests (pytest)
- All frontend components must have unit tests (Jest + React Testing Library)
- All user stories must have E2E tests (Playwright)
- Code coverage target: 80% (backend), 70% (frontend)
- No direct database access from frontend (enforced by architecture)
- No business logic in API routes (enforced by code review)

---

## Definition of Done (Phase 2)

Phase 2 is complete when **ALL** of the following are true:

1. ✅ **Full-stack Todo app works end-to-end**
   - User can access web app in browser
   - User can perform all Level 1, Level 2, Level 3 operations
   - All data persists in Neon PostgreSQL database

2. ✅ **All three feature levels are implemented**
   - Level 1 (Core): Task CRUD, completion status, list view
   - Level 2 (Organization): Priority, tags, search, filter, sort
   - Level 3 (Intelligent): Due dates, recurrence, reminders

3. ✅ **Specs and implementation match exactly**
   - All API endpoints from [sp.api-contract.md](contracts/sp.api-contract.md) are implemented
   - All data model fields from [contracts/sp.data-model.md](contracts/sp.data-model.md) are present
   - All state transitions from [contracts/sp.state-and-lifecycle.md](contracts/sp.state-and-lifecycle.md) work correctly
   - All frontend behaviors from [contracts/sp.frontend-behavior.md](contracts/sp.frontend-behavior.md) are implemented

4. ✅ **Reusable intelligence is in use**
   - At least 2 subagents are actively invoked (Recurrence Reasoning, Reminder Evaluation minimum)
   - At least 1 agent skill is demonstrably used (Recurrence Pattern Validator minimum)
   - All agents log invocations with structured JSON

5. ✅ **System is extensible and agent-ready**
   - Agents use JSON inputs/outputs (no free text)
   - API contracts are versioned (/api/v1/)
   - Schema evolution strategy is documented and followed
   - No hardcoded business logic in frontend or API routes (logic in services/agents)

6. ✅ **All acceptance criteria pass**
   - User Story 1: 4/4 acceptance scenarios pass
   - User Story 2: 5/5 acceptance scenarios pass
   - User Story 3: 5/5 acceptance scenarios pass

7. ✅ **All validation gates pass**
   - Constitution Check: 34/34 requirements met
   - Level 1 Validation Gate: API tests + E2E tests pass
   - Level 2 Validation Gate: No regressions in Level 1, Level 2 tests pass
   - Level 3 Validation Gate: No regressions in Level 1 or 2, Level 3 tests pass

8. ✅ **Performance targets met** (from [contracts/sp.non-functional.md](contracts/sp.non-functional.md))
   - API response time (p95): < 500ms
   - Page load (initial, p95): < 2 seconds
   - Task list rendering (1000 tasks, p95): < 1 second

9. ✅ **Documentation is complete**
   - README.md with setup instructions
   - [sp.quickstart.md](sp.quickstart.md) with developer onboarding
   - API documentation (OpenAPI schema auto-generated)
   - Agent documentation (input/output schemas in [sp.reusable-intelligence.md](contracts/sp.reusable-intelligence.md))

---

## Change Management

**Spec Change Policy** (from constitution):

All spec changes require:
1. **Impact Analysis**: Which features, API endpoints, data models affected?
2. **Version Bump**: MAJOR (breaking), MINOR (additive), PATCH (clarification)
3. **Migration Plan**: How to migrate existing data/code (if breaking change)
4. **No Silent Behavior Changes**: All changes must be documented in spec and communicated

**Example Spec Change Workflow**:
1. User requests: "Add task description character limit to 5000"
2. Impact analysis: Affects [sp.data-model.md](contracts/sp.data-model.md) (validation rule), [sp.api-contract.md](contracts/sp.api-contract.md) (request schema), frontend validation
3. Version bump: MINOR (relaxing constraint, backward compatible)
4. Update specs: Edit data-model.md, api-contract.md, frontend-behavior.md
5. Update implementation: Pydantic model, frontend validation, tests
6. Document change: Add to CHANGELOG.md with version and rationale

---

## Next Steps

1. **Generate [sp.research.md](sp.research.md)**: Document all 7 decisions from Phase 0
2. **Generate [sp.quickstart.md](sp.quickstart.md)**: Developer onboarding guide
3. **Validate Constitution Check**: Re-run after Phase 1 artifacts are complete
4. **Proceed to `/sp.tasks`**: Generate executable task list with dependencies and checkpoints
5. **Optional: Run `/sp.adr`**: Document technology stack architectural decisions (Next.js + FastAPI + SQLModel + Neon)

---

**Plan Complete**: Ready for `/sp.tasks` command to generate implementation task list.
