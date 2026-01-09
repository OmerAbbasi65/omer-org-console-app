<!--
Sync Impact Report - Constitution Update
═══════════════════════════════════════════════════════════════════════════════

Version Change: 1.0.0 → 2.0.0
Rationale: MAJOR version bump - Breaking change from console-only CLI app to full-stack web application with new technology stack and architectural layers

Modified Principles:
  - Project Identity: CLI Console App → Full-Stack Web Application (Phase 2)
  - Technology Stack: Added Next.js (App Router), FastAPI, SQLModel, Neon PostgreSQL
  - Architecture: Added frontend, backend, ORM layers with clear separation of concerns
  - Constitutional Supremacy: Added explicit priority order for artifact conflicts
  - Core Philosophy: Expanded AI-Native design to include agent delegation and reusable intelligence
  - Added: Reusable Intelligence Constitution (BONUS) as first-class constitutional requirement

Sections Added:
  - Project Identity (Phase 2 context)
  - Constitutional Supremacy (priority order)
  - Technology-Specific Constitutional Rules (Frontend, Backend, Data Layer)
  - Reusable Intelligence Constitution (Subagents & Agent Skills)
  - API & Contract Rules
  - Success Definition for Phase 2

Sections Retained:
  - Core Development Philosophy (enhanced for full-stack)
  - Progressive Feature Maturity (3 levels: Core, Organization, Intelligent)
  - Governance (enforcement, amendments, versioning)

Templates Requiring Updates:
  ⚠ plan-template.md - NEEDS UPDATE: Add Phase 2 full-stack structure, API contracts
  ⚠ spec-template.md - NEEDS UPDATE: Add API endpoint requirements, UI behavior specs
  ⚠ tasks-template.md - NEEDS UPDATE: Add frontend/backend separation, API contract tasks
  ✅ phr-template.prompt.md - No changes needed

Follow-up TODOs:
  - Update plan-template.md to include API contract sections
  - Update spec-template.md to include UI behavior and API endpoint requirements
  - Update tasks-template.md to reflect frontend/backend task organization
  - Validate that existing Phase 1 (CLI) implementation remains constitutional under new rules

═══════════════════════════════════════════════════════════════════════════════
-->

# AI-Native Todo Web Application Constitution

## Project Identity

**Project Name**: AI-Native Todo Web Application
**Phase**: Phase 2 — Full-Stack Web Application
**Development Mode**: Spec-Driven, Agentic, AI-Native
**Primary Orchestrator**: Claude (Spec-Kit Plus)

**Technology Stack**:
- **Frontend**: Next.js (App Router)
- **Backend**: FastAPI
- **ORM / Models**: SQLModel
- **Database**: Neon (Serverless PostgreSQL)
- **Bonus Capability**: Reusable Intelligence via Claude Code Subagents & Agent Skills

## Constitutional Supremacy

This constitution is the highest authority for Phase 2 development.

**Priority Order**:

1. This `/sp.constitution`
2. Feature specs (`/sp.features`)
3. API & data contracts
4. UI behavior specs
5. Implementation details

**Resolution Rule**: No artifact may violate a higher-priority rule. In case of conflict, the higher-priority source prevails and the lower-priority artifact MUST be amended.

## Core Development Philosophy

### 1. Spec-First, Full-Stack

**No Code Without Spec (NON-NEGOTIABLE)**

No frontend or backend code may be written without:
- An explicit spec
- Defined contracts (API, schema, or UI behavior)

**Full-Stack Integration Requirement**:
- Frontend and backend MUST be designed together, not sequentially
- API contracts MUST be defined before either side implements
- Schema changes MUST be specified and migrated before code uses them

**Rationale**: Prevents integration mismatches, ensures contract compliance, enables parallel development of frontend and backend teams, and maintains architectural coherence.

### 2. AI-Native Architecture

**Design for Intelligent Delegation**

The system MUST be designed assuming:
- Agents reason over tasks (not just execute commands)
- Logic is inspectable and reusable (not buried in opaque code)
- Behaviors can be delegated to subagents (task planning, recurrence reasoning, query interpretation)
- Data and workflows are structured for agent introspection and automation

**Anti-Pattern**: "Just CRUD Thinking"
- Avoid hardcoded flows that agents cannot reason about
- Prefer declarative logic over imperative scripts
- Design APIs and data models that agents can introspect and manipulate

**Rationale**: Enables progressive automation, facilitates testing, allows the system to evolve from manual operations to autonomous agent-driven workflows, and future-proofs the architecture for agent-native features.

### 3. Progressive Feature Maturity

**Level-Gated Implementation (NON-NEGOTIABLE)**

All features MUST follow this order:

**Level 1 — Core**
- Add / Update / Delete Tasks
- View Task List
- Mark Complete / Incomplete

**Level 2 — Organization**
- Priorities (High / Medium / Low)
- Tags / Categories
- Search, Filter, Sort

**Level 3 — Intelligent**
- Due Dates
- Recurring Tasks
- Time-based Reminders

**Constitutional Constraints**:
- No feature may skip levels
- Each level MUST pass all acceptance criteria before the next unlocks
- Breaking changes to lower levels require re-validation of all higher levels
- All levels MUST remain functional and accessible through both web UI and any retained CLI

**Rationale**: Ensures stable foundation, prevents over-engineering, delivers incremental value, maintains backwards compatibility throughout evolution, and enables independent testing of each maturity level.

## Technology-Specific Constitutional Rules

### Frontend (Next.js)

**Mandatory Architecture**:
- MUST use App Router (not Pages Router)
- MUST separate:
  - UI components (`/components`)
  - Server actions / API calls (`/app/actions` or `/services`)
  - State logic (controlled stores, not implicit)
- MUST NOT access database directly (backend is the single source of truth)
- UI MUST be stateless by default; state lives in backend or controlled stores

**Rationale**: Enforces separation of concerns, ensures testability, prevents tight coupling between UI and data layer, and enables server-side rendering and client-side hydration without conflicts.

### Backend (FastAPI)

**Single Source of Truth**

Backend acts as the single source of truth for all data and business logic.

**Mandatory Architecture**:
- MUST expose RESTful endpoints with clear request/response schemas
- MUST NOT contain business logic in routes (routes are adapters only)
- Logic MUST live in:
  - Services (`/services`)
  - Domain modules (`/domain`)
  - Agent-assisted layers (for intelligent features)

**Rationale**: Prevents business logic leakage into presentation layer, enables independent testing of domain logic, supports future API versioning, and allows agent reasoning over domain models.

### Data Layer (SQLModel + Neon)

**Schema Authority**: SQLModel is the canonical schema definition.

**Database**: Neon (Serverless PostgreSQL)
- Serverless (scales to zero, pay-per-use)
- Persistent (durable storage)
- Single-tenant per project

**Constitutional Constraints**:
- No schema change without migration spec (spec → migration → code)
- No breaking schema changes (only additive changes allowed; deprecate and migrate for removals)
- IDs MUST be globally unique (UUID or composite keys)
- Time fields MUST be timezone-aware (store as UTC)

**Rationale**: Ensures data integrity, prevents data loss during migrations, enables backward-compatible schema evolution, and supports multi-timezone use cases.

## Reusable Intelligence Constitution (BONUS)

**First-Class Artifact**: Reusable intelligence is a first-class artifact, not an afterthought.

### Definition

Reusable intelligence includes:
- Claude Code subagents
- Agent Skills (prompt-as-spec workflows)
- Reasoning workflows (task planning, recurrence logic, query interpretation)

### Rules for Subagents

**Subagents MUST have**:
- Clear responsibility (single, well-defined purpose)
- Explicit inputs / outputs (structured, typed contracts)
- No overlapping authority (each subagent owns a distinct domain)

**Subagents MUST NOT**:
- Access UI directly (UI is presentation layer only)
- Mutate database directly (unless explicitly authorized for their domain)

**Example Subagents**:
- Task-Planning Agent (reasons about dependencies, ordering, priorities)
- Recurrence Reasoning Agent (calculates next occurrence dates)
- Reminder Evaluation Agent (determines when to trigger reminders)
- Query Interpretation Agent (parses search/filter intent into structured queries)

**Rationale**: Enables modular reasoning, prevents cross-domain coupling, supports independent testing and evolution of intelligent features, and allows agents to compose behaviors.

### Agent Skills

**Agent Skills MUST**:
- Be stored in `/reusable/` or `.specify/skills/`
- Be versioned (semver for breaking changes)
- Be context-independent (no hardcoded project-specific paths or secrets)
- Accept structured input (JSON or typed schemas)
- Produce structured output (JSON or typed schemas)

**Skills MUST be reusable across**:
- CLI (command-line interface)
- Web UI (via API calls)
- Future mobile apps
- Future agents (composable workflows)

**Rationale**: Ensures discoverability, prevents duplication, enables cross-platform reuse, and supports agent composition.

## API & Contract Rules

**All frontend ↔ backend communication MUST**:
- Go through documented APIs (no direct database access from frontend)
- Use validated request/response schemas (Pydantic models, TypeScript types)
- Include error handling (structured error responses with codes and messages)

**Contract Specification Requirements**:
- Endpoint path and HTTP method
- Request schema (body, query params, path params)
- Response schema (success and error cases)
- Authentication/authorization requirements
- Rate limiting and throttling rules (if applicable)

**Rationale**: Provides clear integration contracts, enables independent frontend/backend development, supports automated testing and validation, and prevents runtime integration failures.

## Success Definition (Phase 2)

The Phase 2 project is considered complete when **ALL** of the following are true:

1. Full-stack Todo app runs end-to-end (frontend + backend + database)
2. Specs and implementation match exactly (no spec drift)
3. All features are accessible via web UI
4. All three feature levels (Core → Organization → Intelligent) are implemented
5. Reusable intelligence is demonstrably used (at least one subagent or skill)
6. System is extensible for future agents (APIs support agent automation)
7. Documentation is complete and accurate

**Acceptance Process**:
- Each level MUST pass its acceptance gate before the next begins
- Any constitutional violation MUST be resolved before completion
- Spec changes MUST trigger re-validation of affected implementation
- Frontend and backend MUST pass integration tests together

## Governance

### Constitutional Enforcement

**If ambiguity arises**:
1. Stop
2. Re-specify (do not guess or implement without clarity)
3. Document the clarification in the spec or an ADR

**Amendment Process**:
- Amendments require explicit documentation in `history/adr/`
- Constitutional changes MUST include:
  - Rationale for change
  - Impact assessment (which features/specs affected)
  - Migration plan (if breaking changes introduced)
  - Version increment (MAJOR for breaking, MINOR for additions, PATCH for clarifications)
- All PRs/reviews MUST verify constitutional compliance

**Complexity Justification**:
- Any violation of constitutional constraints MUST be justified in writing
- Justification MUST include:
  - What constraint is violated and why
  - Why simpler alternatives were rejected
  - Mitigation plan to minimize impact
- Complexity MUST be approved before implementation

**Compliance & Review**:
- All specs MUST reference constitutional principles they implement
- All code reviews MUST check constitutional alignment
- Use `CLAUDE.md` for runtime development guidance
- Constitutional violations discovered post-implementation MUST be logged as technical debt and prioritized for remediation

**Version**: 2.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-09
