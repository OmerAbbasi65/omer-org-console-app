<!--
Sync Impact Report - Constitution Update
═══════════════════════════════════════════════════════════════════════════════

Version Change: [Initial Version] → 1.0.0
Rationale: First formal constitution ratification from template

Modified Principles:
  - Replaced all placeholder principles with concrete AI-Native Todo App principles
  - Added: Spec-First Development, AI-Native Design, Incremental Feature Progression
  - Added: Command-Driven Architecture, Data Model Evolution, Testing & Validation
  - Added: Feature Levels (Basic → Intermediate → Advanced)

Sections Added:
  - Project Identity
  - Core Development Philosophy
  - Feature Constitution (3 levels with specific capabilities and constraints)
  - Command-Driven Architecture Rule
  - Data Model Constitution
  - Documentation & Output Rules
  - Success Definition
  - Constitutional Priority Order

Sections Removed:
  - None (this is initial population)

Templates Requiring Updates:
  ✅ plan-template.md - Constitution Check section already present and generic
  ✅ spec-template.md - User Scenarios and Requirements align with constitution
  ✅ tasks-template.md - Task structure aligns with incremental progression
  ✅ phr-template.prompt.md - No constitution-specific changes needed

Follow-up TODOs:
  - None: All placeholders filled with concrete values

═══════════════════════════════════════════════════════════════════════════════
-->

# AI-Native Todo Console Application Constitution

## Core Principles

### I. Spec-First Development

**Spec Before Code (NON-NEGOTIABLE)**

No code may be written before a corresponding spec exists. Every feature MUST have:
- Clear intent and purpose
- Defined inputs and outputs
- Explicit constraints
- Measurable acceptance criteria

**Rationale**: Prevents scope creep, ensures architectural alignment, and provides a contract for validation. Specs serve as living documentation and enable AI agents to reason about intent rather than guess implementation.

### II. AI-Native Design

**Declarative Over Imperative**

Treat tasks, commands, and workflows as structured data. Design for machine readability and agent automation:
- Prefer declarative logic over hard-coded behavior
- Use structured data formats (JSON, YAML) for configuration
- Enable future agent automation (reasoning over tasks, reminders, recurrence)
- Design APIs and data models that agents can introspect and manipulate

**Rationale**: Enables progressive automation, facilitates testing, and allows the system to evolve from manual CLI operations to autonomous agent-driven workflows.

### III. Incremental Feature Progression

**Level-Gated Implementation (NON-NEGOTIABLE)**

Implement features strictly in this order with blocking gates:

1. **Basic Level** - Core Essentials (Add, Delete, Update, View, Complete/Incomplete)
2. **Intermediate Level** - Organization & Usability (Priorities, Tags, Search, Filter, Sort)
3. **Advanced Level** - Intelligent Features (Recurring Tasks, Due Dates, Time Reminders)

**Constitutional Constraints**:
- No advanced feature may bypass or break earlier layers
- Each level MUST pass all acceptance criteria before the next unlocks
- Breaking changes to lower levels require re-validation of all higher levels

**Rationale**: Ensures stable foundation, prevents over-engineering, delivers incremental value, and maintains backwards compatibility throughout evolution.

### IV. Command-Driven Architecture

**Explicit Commands Required**

All functionality MUST be accessible via explicit commands. No implicit behavior or hidden features.

**Each command MUST define**:
- Name (clear, action-oriented verb)
- Arguments schema (typed, validated)
- Validation rules (input constraints)
- Success & failure outputs (structured, predictable)

**Example Commands**: `add`, `update`, `delete`, `list`, `complete`, `filter`, `sort`

**Rationale**: Provides clear contracts for testing, documentation, and future API generation. Enables command-line interface, scripting, and agent automation. Prevents hidden behaviors that complicate reasoning.

### V. Data Model Evolution

**Schema Stability & Backward Compatibility**

Tasks MUST be represented as structured objects, not free text.

**Minimum evolving schema**:
```json
{
  "id": "string",
  "title": "string",
  "description": "string?",
  "completed": "boolean",
  "priority": "high|medium|low?",
  "tags": ["string"],
  "dueDate": "ISO-8601?",
  "recurrence": "none|daily|weekly|monthly?"
}
```

**Constitutional Constraints**:
- Schema MUST evolve incrementally (never break backward compatibility)
- Optional fields marked with `?` suffix
- Each task MUST have a unique identifier
- Completion status MUST be boolean (never nullable)
- Storage abstraction required (in-memory first, file-based later)

**Rationale**: Enables data migration, supports versioning, allows incremental feature addition without data loss, and provides clear contracts for agents and APIs.

### VI. Testing & Validation

**Define Before Implement**

Every feature MUST define before implementation:
- Happy path scenarios
- Edge cases (boundary conditions)
- Failure modes (error scenarios)

**Testing Approach**:
- Manual CLI testing is acceptable
- Specs MUST include example command invocations
- Each command MUST demonstrate success and failure cases
- Acceptance criteria MUST be measurable and verifiable

**Rationale**: Ensures quality gates, prevents regressions, documents expected behavior, and enables confident refactoring. Specs double as test documentation.

### VII. Simplicity & YAGNI

**Minimum Viable Implementation**

Start simple. Implement only what is specified. Do not:
- Hardcode logic that should be configurable
- Introduce UI frameworks (this is a console app)
- Skip error handling or edge cases in specs
- Implement features not explicitly listed in the progression
- Add features speculatively for future use

**Rationale**: Prevents over-engineering, reduces maintenance burden, keeps codebase understandable, and allows architecture to emerge from actual needs rather than hypothetical ones.

## Feature Constitution

### Level 1 — Basic (Core Essentials)

**Status**: MANDATORY and BLOCKING for all other levels

**Required Capabilities**:
- Add Task
- Delete Task
- Update Task
- View Task List
- Mark Task as Complete / Incomplete

**Constitutional Constraints**:
- Each task MUST have a unique identifier
- Completion status MUST be boolean (true/false)
- Task storage MUST be abstracted (in-memory first, file-based later)
- No feature from Intermediate or Advanced may be implemented until Basic is complete

**Acceptance Gate**: All Basic commands functional, tested, and documented before proceeding to Intermediate.

### Level 2 — Intermediate (Organization & Usability)

**Status**: UNLOCKED only after Level 1 is complete and stable

**Required Capabilities**:
- Priorities (High / Medium / Low)
- Tags or Categories (e.g., work, home)
- Search by keyword
- Filter by: Status, Priority, Category (composable)
- Sort by: Due date, Priority, Alphabetical order

**Constitutional Constraints**:
- Priority and tags are OPTIONAL fields (nullable in data model)
- Filters MUST be composable (e.g., `priority=high AND status=incomplete`)
- Sorting MUST NOT mutate underlying data order unless explicitly saved
- All Basic features MUST remain functional

**Acceptance Gate**: All Intermediate commands functional, composable filters working, no regressions in Basic level.

### Level 3 — Advanced (Intelligent Features)

**Status**: UNLOCKED only after Level 2 passes all acceptance criteria

**Required Capabilities**:
- Recurring Tasks (Daily / Weekly / Monthly patterns)
- Auto-rescheduling on completion
- Due Dates (date and optional time, ISO-8601 format)
- Time Reminders (console-based notifications via polling or scheduler)
- Browser or OS notifications (OPTIONAL, non-blocking)

**Constitutional Constraints**:
- Recurrence rules MUST be declarative (not hardcoded logic)
- Reminder logic MUST be separable from task logic (modular design)
- System MUST handle missed reminders gracefully (no crashes, clear error messages)
- All Basic and Intermediate features MUST remain functional

**Acceptance Gate**: Recurring tasks generate correctly, reminders trigger reliably, no regressions in Basic or Intermediate levels.

## Documentation & Output Rules

**Documentation Structure**:
- Specs stored in `/specs/<feature-name>/spec.md`
- Reusable schemas in `/specs/reusable/`
- Command documentation in `/docs/commands.md`
- No duplication of logic across specs

**Output Requirements**:
- Claude MUST write specs before code
- Claude MUST avoid duplicating logic across specs
- Claude MUST place reusable schemas in `/specs/reusable/`
- Claude MUST keep commands documented in `/docs/commands.md`

**Rationale**: Centralized documentation, single source of truth, enables discoverability, supports onboarding and maintenance.

## Success Definition

**Project Completion Criteria**:

The project is considered complete when ALL of the following are true:

1. All three feature levels (Basic → Intermediate → Advanced) are implemented
2. Specs and implementation match 1:1 (no spec drift)
3. The app can be used entirely via CLI (no GUI dependencies)
4. No feature violates this constitution
5. All acceptance gates for all three levels have passed
6. Documentation is complete and accurate

**Acceptance Process**:
- Each level MUST pass its acceptance gate before the next begins
- Any constitutional violation MUST be resolved before completion
- Spec changes MUST trigger re-validation of affected implementation

## Governance

**Constitutional Supremacy**

This constitution supersedes all other practices, patterns, and preferences. In the event of conflict, the resolution order is:

1. This constitution (highest authority)
2. Feature specs (must align with constitution)
3. Implementation plans (must align with specs and constitution)
4. Code (must align with plans, specs, and constitution)

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
- Use `CLAUDE.md` (this file) for runtime development guidance
- Constitutional violations discovered post-implementation MUST be logged as technical debt and prioritized for remediation

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
