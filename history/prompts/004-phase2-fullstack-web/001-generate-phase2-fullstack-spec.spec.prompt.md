---
id: 001
title: Generate Phase 2 Full-Stack Specification Set
stage: spec
date: 2026-01-09
surface: agent
model: claude-sonnet-4-5
feature: 004-phase2-fullstack-web
branch: 004-phase2-fullstack-web
user: Omer Abbasi
command: /sp.specify
labels: ["spec", "phase2", "full-stack", "nextjs", "fastapi", "sqlmodel", "neon", "reusable-intelligence", "ai-native"]
links:
  spec: specs/004-phase2-fullstack-web/sp.requirements.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-phase2-fullstack-web/sp.requirements.md
  - specs/004-phase2-fullstack-web/contracts/sp.api-contract.md
  - specs/004-phase2-fullstack-web/contracts/sp.data-model.md
  - specs/004-phase2-fullstack-web/contracts/sp.state-and-lifecycle.md
  - specs/004-phase2-fullstack-web/contracts/sp.frontend-behavior.md
  - specs/004-phase2-fullstack-web/contracts/sp.reusable-intelligence.md
  - specs/004-phase2-fullstack-web/contracts/sp.non-functional.md
  - specs/004-phase2-fullstack-web/checklists/requirements.md
tests:
  - null
---

## Prompt

— Specification Generation Prompt (Phase 2)
Role

You are Claude, acting as a principal full-stack software architect in an AI-native, spec-driven development workflow using Spec-Kit Plus.

You must strictly obey:

/sp.constitution (Phase 2 — Full-Stack Web)

Feature progression rules (Level 1 → Level 2 → Level 3)

Spec-first discipline (no code before specs)

Reusable intelligence requirements

Objective

Produce a complete, implementation-ready specification set for a Full-Stack Todo Web Application built with:

Next.js (App Router)

FastAPI

SQLModel

Neon (PostgreSQL)

Claude Code Subagents & Agent Skills

The specification set must include:

1. /sp.requirements.md - Main requirements document with user stories, functional requirements, success criteria
2. /sp.api-contract.md - RESTful API endpoints with request/response schemas
3. /sp.data-model.md - Canonical data models (Task, Recurrence, Reminder) with SQLModel schemas
4. /sp.state-and-lifecycle.md - Task lifecycle states, state transitions, recurring task logic
5. /sp.frontend-behavior.md - Page-level behavior, data-fetching, loading/error states, client-API interaction
6. /sp.reusable-intelligence.md - Subagents (Task-Planning, Recurrence Reasoning, Reminder Evaluation, Query Interpretation) and Agent Skills
7. /sp.non-functional.md - Performance, reliability, extensibility, security, observability requirements

Behavioral Constraints

You MUST:

Follow the constitution exactly

Be explicit and declarative

Treat specs as enforceable contracts

Call out edge cases

You MUST NOT:

Write code

Skip acceptance criteria

Merge frontend and backend concerns

Introduce features not listed

Assume implementation details

Output Rules

Use Markdown

Clear headings

Structured lists

No pseudocode unless absolutely necessary

No repetition across specs

Completion Condition

Stop once all required spec artifacts are fully defined.

Do not:

Summarize

Explain your reasoning

Ask questions

Suggest next steps

## Response snapshot

Successfully generated comprehensive Phase 2 Full-Stack Todo Web Application specification set with 7 documents:

**Main Requirements** (sp.requirements.md):
- 3 prioritized user stories (P1: Basic Task Management, P2: Task Organization, P3: Intelligent Scheduling)
- 30 functional requirements organized by feature level (Core, Organization, Intelligent, Cross-Cutting)
- 10 measurable success criteria (technology-agnostic, user-focused)
- 4 key entities (Task, Recurrence Pattern, Reminder, User Session)
- 8 edge cases documented with expected behaviors
- 7 assumptions documented (single-user, browser support, network latency, etc.)

**API Contract** (sp.api-contract.md):
- 11 RESTful endpoints covering CRUD operations, filtering, search, recurring task completion, overdue/reminder queries
- Complete request/response schemas with validation rules
- Error response schema with structured error codes
- HTTP status codes and error handling conventions

**Data Model** (sp.data-model.md):
- Task model with 11 fields (id, title, description, completed, priority, tags, due_date, recurrence, parent_id, created_at, updated_at)
- 6 indexes for performance (primary key, completed, due_date, priority, composite, GIN on tags)
- 4 check constraints for data integrity
- Recurrence logic and instance generation rules
- Schema evolution strategy with backward compatibility guarantees

**State and Lifecycle** (sp.state-and-lifecycle.md):
- 2 primary states (Active, Completed) and 5 derived states (Overdue, Upcoming, Scheduled, Unscheduled, Recurring)
- State transition rules for basic and recurring tasks
- Recurring instance generation logic with edge case handling
- Reminder triggering semantics with 5 reminder states
- State observability with 7 log event types

**Frontend Behavior** (sp.frontend-behavior.md):
- 3 pages defined (Home, Task Detail, modals) with data-fetching strategies
- Loading and error state patterns for all interactions
- Form submission behavior with client-side validation
- Optimistic UI update rules for 4 operations
- Client ↔ API interaction rules with retry logic
- Accessibility requirements (WCAG AA standards)

**Reusable Intelligence** (sp.reusable-intelligence.md):
- 4 subagents with explicit responsibilities, inputs/outputs, reasoning processes
- 4 agent skills with input/output schemas, versioning rules (semver), reusability constraints
- Cross-platform reusability (CLI, Web UI, mobile, future agents)
- Observability with structured logging for all agent invocations

**Non-Functional Requirements** (sp.non-functional.md):
- Performance: 7 latency targets (p95/p99), 4 throughput metrics, 5 resource constraints
- Reliability: 99.5% availability target, error budget policy, 6 failure mode scenarios
- Extensibility: API versioning strategy, schema evolution rules
- Security: Input validation rules, encryption standards, future auth strategy
- Observability: Structured logging schema, 11 log event types, health check endpoints

**Validation Results** (checklists/requirements.md):
- ✅ All 16 checklist criteria passed
- ✅ No [NEEDS CLARIFICATION] markers (all requirements concrete)
- ✅ All acceptance scenarios defined with Given-When-Then format
- ✅ Success criteria are measurable and technology-agnostic
- ✅ Constitutional compliance verified (spec-first, AI-native, progressive maturity)

## Outcome

- ✅ Impact: Complete, implementation-ready specification set for Phase 2 Full-Stack Todo Web Application covering all constitutional requirements (Next.js + FastAPI + SQLModel + Neon + Reusable Intelligence)
- 🧪 Tests: N/A (specification phase, no executable tests)
- 📁 Files: Created 8 files (1 main requirements, 6 contract specifications, 1 validation checklist) in specs/004-phase2-fullstack-web/
- 🔁 Next prompts: Ready for `/sp.plan` to create architectural implementation plan; Consider `/sp.adr` to document technology stack architectural decisions (Next.js, FastAPI, SQLModel, Neon)
- 🧠 Reflection: Specification successfully balances constitutional requirements (AI-native, reusable intelligence) with pragmatic Phase 2 scope (single-user, no multi-tenancy). Reusable Intelligence specification elevates Phase 2 beyond "just another CRUD app" by making agent reasoning a first-class concern. All 7 documents are internally consistent and reference each other appropriately.

## Evaluation notes (flywheel)

- Failure modes observed: None - All specification documents created successfully without clarification needed from user
- Graders run and results (PASS/FAIL): PASS - Validation checklist confirms all 16 criteria met; No [NEEDS CLARIFICATION] markers; All requirements testable and unambiguous
- Prompt variant (if applicable): Used detailed multi-document specification approach (7 separate contract files) rather than monolithic spec file for better separation of concerns
- Next experiment (smallest change to try): Monitor whether 7-document structure provides better clarity during planning phase vs. potential navigation overhead; Validate whether Reusable Intelligence specifications translate effectively into actual subagent implementations during `/sp.implement`
