# Implementation Plan: AI-Native Todo Console Application

**Branch**: `001-todo-app-full` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-app-full/spec.md`

## Summary

Implement a console-based todo application with three progressive feature levels (Basic → Intermediate → Advanced), following spec-driven, AI-native architecture principles. The application enables task management through CLI commands with file-based persistence, priority/tag organization, and intelligent time-based features.

**Primary Requirement**: Build incrementally with blocking gates between levels to ensure stable foundation.

**Technical Approach**: Layered architecture (CLI → Domain → Storage) with declarative data models, enabling future agent automation and extensibility.

---

## Technical Context

**Language/Version**: Language-agnostic (Python 3.11+, Node.js 18+, Go 1.21+, or Rust 1.75+ recommended)
**Primary Dependencies**: Standard library only (JSON parsing, file I/O, datetime handling, CLI arg parsing)
**Storage**: JSON file at `~/.todo-data.json` in user's home directory
**Testing**: Language-native test framework (pytest, Jest, go test, cargo test)
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: Single console application
**Performance Goals**:
- Command execution < 3 seconds (NFR-005)
- App startup < 2 seconds (NFR-004)
- Support 1,000+ tasks without degradation (SC-005)

**Constraints**:
- Console-only interface (no GUI, web, or mobile)
- Offline-first (no network dependencies)
- Single-user (no authentication or multi-user)
- File-based storage only (no database)

**Scale/Scope**: Target 10-500 tasks per user, single executable, < 5MB binary size

---

## Constitution Check

*GATE: Must pass before implementation. Re-check after design changes.*

### Principle I - Spec-First Development
✅ **PASS**: Complete specification exists at `spec.md` with 35 functional requirements, 17 success criteria, and acceptance scenarios for all features.

### Principle II - AI-Native Design
✅ **PASS**: Tasks represented as structured JSON with declarative recurrence rules (enum-based, not hardcoded logic). CLI commands follow predictable patterns for agent automation.

### Principle III - Incremental Feature Progression
✅ **PASS**: Plan enforces Level 1 (Basic) → Level 2 (Intermediate) → Level 3 (Advanced) with explicit gates and no level-skipping.

### Principle IV - Command-Driven Architecture
✅ **PASS**: All functionality accessible via explicit CLI commands (add, list, update, delete, complete, filter, sort, etc.) with defined contracts in `contracts/cli-commands.md`.

### Principle V - Data Model Evolution
✅ **PASS**: Task schema defined in `data-model.md` with optional fields marked, backward compatibility strategy documented, and evolution path specified.

### Principle VI - Testing & Validation
✅ **PASS**: Testing strategy covers unit, integration, and acceptance levels. Each feature level has acceptance criteria mapped from spec scenarios.

### Principle VII - Simplicity & YAGNI
✅ **PASS**: No speculative features added. Implementation scoped to exact requirements. No UI frameworks, no cloud dependencies, no over-abstraction.

**GATE STATUS**: ✅ ALL CHECKS PASSED - Proceed with implementation

---

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-app-full/
├── spec.md                  # Feature specification
├── plan.md                  # This file (/sp.plan output)
├── research.md              # Phase 0 output (decisions and rationale)
├── data-model.md            # Phase 1 output (Task entity schema)
├── quickstart.md            # Phase 1 output (developer guide)
├── contracts/               # Phase 1 output (CLI command contracts)
│   └── cli-commands.md
└── tasks.md                 # Phase 2 output (/sp.tasks - NOT created yet)
```

### Source Code (repository root)

```text
src/
├── cli/
│   ├── parser               # Argument parsing and validation
│   ├── commands/            # Command implementations (add, list, update, etc.)
│   │   ├── level1/          # Basic commands (add, list, update, delete, complete)
│   │   ├── level2/          # Intermediate commands (filter, search, sort, set-priority)
│   │   └── level3/          # Advanced commands (set-due, set-recurrence, set-reminder)
│   └── formatter            # Output formatting (tables, success/error messages)
├── domain/
│   ├── task                 # Task entity + validation logic
│   ├── task-filter          # Filter logic (status, priority, tag, keyword)
│   ├── task-sort            # Sort logic (priority, title, dueDate, createdAt)
│   └── recurrence           # Recurrence calculation (daily, weekly, monthly)
├── storage/
│   ├── storage-interface    # Abstract storage contract
│   └── file-storage         # JSON file persistence implementation
├── reminder/
│   └── reminder-service     # 60-second polling for due reminders (Level 3)
└── main                     # Entry point (CLI dispatcher)

tests/
├── unit/
│   ├── domain/              # Task, filter, sort, recurrence tests
│   └── storage/             # Storage interface tests (with mocks)
├── integration/
│   └── commands/            # End-to-end command tests
└── acceptance/
    ├── level1/              # US1 acceptance scenarios
    ├── level2/              # US2 acceptance scenarios
    └── level3/              # US3 acceptance scenarios
```

**Structure Decision**: Single project structure selected. Console application does not require frontend/backend separation or mobile-specific organization.

---

## Complexity Tracking

> **No constitutional violations** - all principles satisfied without justification needed.

---

## Feature Rollout Plan

### Phase 1: Level 1 - Basic (MANDATORY, BLOCKING)

**Goal**: Deliver MVP with core task CRUD and file persistence.

**Features** (from FR-001 to FR-012):
1. Add task with title and optional description
2. Generate unique timestamp-based task ID
3. View all tasks in tabular format
4. Update task title and description
5. Mark task as complete/incomplete
6. Delete task by ID
7. Persist tasks to `~/.todo-data.json`
8. Validate inputs (non-empty title, ID exists)
9. Display clear error messages

**Dependencies**:
- None (foundational layer)

**Implementation Order**:
1. Data model: Task entity with Level 1 fields
2. Storage: FileStorage with JSON read/write
3. CLI commands: add → list → update → complete → incomplete → delete
4. Tests: Unit tests for Task validation, integration tests for each command, acceptance tests for US1

**Acceptance Gate**: All 6 scenarios from US1 (spec.md lines 28-35) pass + SC-001 to SC-006 verified.

**Blocked**: Level 2 cannot start until this gate passes.

---

### Phase 2: Level 2 - Intermediate (after Level 1 complete)

**Goal**: Add organization and discovery capabilities.

**Features** (from FR-013 to FR-024):
1. Priority field (high/medium/low)
2. Tags field (array of strings)
3. Search by keyword (case-insensitive partial match)
4. Filter by status, priority, tag (composable with AND)
5. Sort by priority, title, dueDate, createdAt
6. Enhanced add command with priority/tags
7. Dedicated set-priority and set-tags commands

**Dependencies**:
- Level 1 complete (extends Task entity and add command)

**Implementation Order**:
1. Data model: Add `priority` and `tags` to Task
2. Domain logic: TaskFilter (AND composition) + TaskSort
3. CLI commands: enhance add → set-priority → set-tags → search → filter → sort
4. Tests: Unit tests for filter/sort logic, integration tests for new commands, acceptance tests for US2

**Acceptance Gate**: All 6 scenarios from US2 (spec.md lines 47-54) pass + SC-007 to SC-011 verified + no Level 1 regressions.

**Blocked**: Level 3 cannot start until this gate passes.

---

### Phase 3: Level 3 - Advanced (after Level 2 complete)

**Goal**: Add time-based intelligence and automation.

**Features** (from FR-025 to FR-035):
1. Due date field (ISO-8601 datetime)
2. Recurrence field (none/daily/weekly/monthly)
3. Reminder time field (ISO-8601 datetime)
4. Recurring task auto-reschedule on completion
5. 60-second polling for reminder notifications
6. Overdue task indicators in list view
7. Enhanced add command with due/recurrence/remind
8. Dedicated set-due, set-recurrence, set-reminder commands

**Dependencies**:
- Level 2 complete (extends Task entity and add command)

**Implementation Order**:
1. Data model: Add `dueDate`, `recurrence`, `reminderTime`, `lastNotified` to Task
2. Domain logic: Recurrence date calculation + overdue detection
3. Reminder service: 60-second polling background thread
4. CLI commands: enhance add/complete → set-due → set-recurrence → set-reminder → enhance list
5. Tests: Unit tests for recurrence logic, integration tests for reminder polling, acceptance tests for US3

**Acceptance Gate**: All 6 scenarios from US3 (spec.md lines 66-73) pass + SC-012 to SC-017 verified + no Level 1/2 regressions.

**Completion**: All three levels functional, application ready for production use.

---

## Architectural Decisions

### Decision 1: Task ID Generation

**Options Considered**:
1. Sequential integers (1, 2, 3...)
2. UUID v4 (globally unique)
3. Timestamp-based (unix milliseconds)
4. Short random alphanumeric

**Chosen**: Timestamp-based with format `task-<unix-timestamp-ms>`

**Tradeoffs**:
- **Pro**: Chronologically sortable, unique for single-user, no counter management
- **Pro**: No external library needed (system time only)
- **Con**: Longer than sequential (but still readable)
- **Con**: Collision possible if two tasks created in same millisecond (acceptable risk for single-user CLI)

**Rationale**: Balances uniqueness, readability, and chronological ordering without requiring persistent counter or complex UUID library. Aligns with clarification decision from `/sp.clarify`.

---

### Decision 2: Storage Abstraction

**Options Considered**:
1. Direct file I/O in each command
2. Repository pattern with full CRUD interface
3. Minimal storage interface (load/save/ensure)

**Chosen**: Minimal storage interface with 3 methods

**Interface**:
```
Storage {
  loadTasks() → Task[]
  saveTasks(tasks: Task[]) → void
  ensureStorageExists() → void
}
```

**Tradeoffs**:
- **Pro**: Testable (can mock storage in command tests)
- **Pro**: Future-proof (can swap file → database without changing commands)
- **Pro**: Minimal (only 3 methods needed)
- **Con**: Extra abstraction layer (but negligible complexity)

**Rationale**: Constitutional requirement (Principle V: "Storage abstraction required"). Enables testing and future extensibility without over-engineering.

**Implementation Details**:
- File location: `~/.todo-data.json` (user home directory)
- Format: Pretty-printed JSON (2-space indent)
- Atomic writes: Write to `.todo-data.json.tmp`, then rename
- Error handling: Create if missing, validate JSON on load, fallback to empty array if corrupted

---

### Decision 3: Recurrence Modeling

**Options Considered**:
1. Enum + hardcoded date calculation
2. Cron-like expression parsing
3. Rule-based interval system

**Chosen**: Enum-based declarative model + date calculation functions

**Data Model**:
```json
{
  "recurrence": "none" | "daily" | "weekly" | "monthly",
  "dueDate": "ISO-8601 datetime"
}
```

**Calculation Logic**:
- **daily**: `dueDate + 1 day`
- **weekly**: `dueDate + 7 days`
- **monthly**: `dueDate + 1 month` (handle month-end edge cases)

**Behavior on Completion**:
1. If `recurrence != "none"`: Calculate next `dueDate`, reset `completed = false`
2. If `recurrence == "none"`: Set `completed = true`

**Tradeoffs**:
- **Pro**: Declarative (recurrence stored as data, not code)
- **Pro**: Simple (covers daily/weekly/monthly without complexity)
- **Pro**: Predictable (clear calculation rules)
- **Con**: Limited to 3 patterns (but meets requirements)

**Rationale**: Satisfies FR-035 ("recurrence rules MUST be stored as declarative data"). Extensible by adding enum values later.

---

### Decision 4: Reminder Triggering

**Options Considered**:
1. Polling (check every N seconds)
2. Event-driven (timer callbacks per task)
3. On-command check (only when user runs command)

**Chosen**: 60-second polling with background thread/timer

**Implementation**:
- Background thread wakes every 60 seconds
- Check all tasks where `reminderTime <= currentTime AND completed == false`
- Display console notification: `🔔 REMINDER: [title] is due at [time]`
- Update `lastNotified` to prevent duplicate alerts

**Tradeoffs**:
- **Pro**: Simple to implement
- **Pro**: Meets SC-014 ("within 60 seconds")
- **Pro**: Low overhead (1 check per minute)
- **Con**: Requires background thread (but acceptable for foreground app)
- **Con**: No notifications if app not running (per FR-032: acceptable)

**Rationale**: Balances simplicity and responsiveness. Aligns with clarification decision (60-second interval).

---

### Decision 5: CLI Output Format

**Options Considered**:
1. Plain text (unstructured)
2. JSON output (machine-readable)
3. Tabular output (ASCII tables)

**Chosen**: Tabular output with ASCII borders

**Example**:
```
ID                   | TITLE              | STATUS
---------------------|--------------------|-----------
task-1735707600000   | Buy groceries      | Incomplete
task-1735707601000   | Deploy app         | Complete
```

**Tradeoffs**:
- **Pro**: Readable and scannable for humans
- **Pro**: Consistent visual format across commands
- **Con**: Harder to parse programmatically (but CLI is human-first)

**Rationale**: Follows CLI UX best practices (researched in `research.md`). Can add `--json` flag later if scripting needed.

---

## Testing & Validation Strategy

### Test Pyramid

```
      ┌─────────────────┐
      │  Acceptance (6) │  ← Spec scenarios (US1, US2, US3)
      └─────────────────┘
     ┌───────────────────┐
     │  Integration (18) │  ← Command end-to-end tests
     └───────────────────┘
    ┌─────────────────────┐
    │   Unit (40+)        │  ← Domain logic, validation, storage
    └─────────────────────┘
```

---

### Level 1 Validation

**Acceptance Tests** (from US1):
1. Create task → verify ID generated and task appears in list
2. List tasks → verify all tasks displayed with ID, title, status
3. Update task → verify title changed
4. Complete task → verify status = complete
5. Incomplete task → verify status = incomplete
6. Delete task → verify task removed

**Integration Tests**:
- `add "title"` → verify storage updated
- `list` → verify output format matches contract
- `update <id> --title "new"` → verify storage updated
- `complete <id>` → verify completed=true in storage
- `incomplete <id>` → verify completed=false in storage
- `delete <id>` → verify task removed from storage

**Unit Tests**:
- Task validation: non-empty title, max length constraints
- ID generation: format matches `task-<timestamp>`
- FileStorage: load/save/atomic write operations
- Error handling: invalid ID, corrupted JSON, disk full

**Success Criteria Validation**:
- SC-001: Measure `add` command execution time < 5 seconds
- SC-002: Measure `list` command execution time < 2 seconds
- SC-003: Measure `update/complete/delete` < 5 seconds
- SC-004: Restart app, verify all tasks still present (persistence)
- SC-005: Create 1,000 tasks, verify `list` performance
- SC-006: Trigger errors (empty title, invalid ID), verify messages clear

---

### Level 2 Validation

**Acceptance Tests** (from US2):
1. Add with priority/tags → verify fields set correctly
2. Filter by priority → verify only matching tasks shown
3. Filter by tag → verify only tagged tasks shown
4. Search keyword → verify partial match works
5. Sort by priority → verify order (high → medium → low)
6. Composable filter → verify AND logic (priority + status)

**Integration Tests**:
- `add "title" --priority high --tags work` → verify storage
- `filter --priority high` → verify output only shows high-priority
- `filter --tag work` → verify output only shows work-tagged
- `search "keyword"` → verify case-insensitive partial match
- `sort --by priority` → verify descending order
- `filter --priority high --status incomplete` → verify AND composition

**Unit Tests**:
- Priority validation: rejects invalid values
- Tag validation: max length enforcement
- TaskFilter: AND logic correctness
- TaskSort: ordering correctness for each field
- Search: case-insensitive partial matching

**Success Criteria Validation**:
- SC-007: Create 100 tasks, measure `search` < 3 seconds
- SC-008: Apply multi-filter, measure < 2 seconds
- SC-009: Measure `sort` < 2 seconds
- SC-010: Manual usability test (95% success with priority/tags)
- SC-011: Verify filter/sort don't corrupt storage

---

### Level 3 Validation

**Acceptance Tests** (from US3):
1. Add with due date → verify field set
2. Add recurring task → verify recurrence field set
3. Complete recurring task → verify due date advances, status resets
4. Reminder notification → verify console output appears
5. Sort by due date → verify chronological order
6. List overdue tasks → verify indicator shown

**Integration Tests**:
- `add "title" --due 2026-01-15T17:00:00` → verify storage
- `add "title" --recurrence daily --due <date>` → verify storage
- `complete <recurring-id>` → verify dueDate advanced, completed=false
- Wait 60 seconds with reminder due → verify notification printed
- `list` with overdue task → verify "OVERDUE" indicator
- `set-due <id> <date>` → verify storage updated

**Unit Tests**:
- ISO-8601 date validation
- Recurrence calculation: daily (+1 day), weekly (+7 days), monthly (+1 month)
- Recurring task reset logic on completion
- Overdue detection: `dueDate < now AND !completed`
- Reminder check: `reminderTime <= now AND !notified`

**Success Criteria Validation**:
- SC-012: Measure `add` with due/remind < 10 seconds
- SC-013: Test recurring completion 10 times, verify 100% reschedule
- SC-014: Set reminder, measure trigger time <= 60 seconds from scheduled
- SC-015: Test edge cases (missed reminder, invalid date), verify no crashes
- SC-016: Manual user feedback collection (80% deadline reduction)
- SC-017: Create overdue task, verify indicator visible in `list`

---

### Edge Case Validation

**From spec.md Edge Cases**:
1. Empty title → Error: "Title cannot be empty"
2. Non-existent ID → Error: "Task '<id>' not found"
3. Invalid priority → Error: "Priority must be high/medium/low"
4. Invalid date format → Error: "Invalid date format. Use ISO-8601"
5. Unsupported recurrence → Error: "Recurrence must be daily/weekly/monthly"
6. Corrupted storage file → Fallback to empty array, log warning
7. Zero filter matches → Output: "No tasks found matching criteria"
8. Sort by missing field → Tasks with null values appear last
9. Missed reminder (app closed) → No notification, no crash on restart
10. Delete recurring task → Task removed permanently, no rescheduling

**Test Coverage**: Create dedicated edge case test suite covering all 10 scenarios.

---

## Synthesis: Convergence of Specs, Commands, and Data

### Specification → Implementation Mapping

| Spec Element | Implementation Artifact | Mapping Rule |
|--------------|------------------------|--------------|
| User Story (US1, US2, US3) | Acceptance Test Suite | 1:1 (each scenario → test) |
| Functional Requirement (FR-001 to FR-035) | Command or Domain Logic | 1:1 (each FR → function/method) |
| Success Criterion (SC-001 to SC-017) | Performance/Quality Test | 1:1 (each SC → verification test) |
| Edge Case | Error Handling + Test | 1:1 (each case → validation + test) |
| Clarification Decision | Implementation Detail | Direct (ID format, storage location, etc.) |

---

### Command → Data Model → Storage Flow

**Example: Add Command with Priority**

```
User Input:
  todo add "Deploy app" --priority high --tags work,urgent

Flow:
1. CLI Parser validates arguments (title non-empty, priority valid)
2. CLI Command creates Task object:
   {
     id: generateTimestampId(),
     title: "Deploy app",
     description: null,
     completed: false,
     priority: "high",
     tags: ["work", "urgent"],
     dueDate: null,
     recurrence: "none",
     reminderTime: null,
     lastNotified: null,
     createdAt: now(),
     updatedAt: now()
   }
3. Task validates itself (title length, priority enum, tag lengths)
4. Storage loads existing tasks from ~/.todo-data.json
5. Storage appends new task to array
6. Storage saves updated array (atomic write)
7. CLI Formatter outputs success message
```

**This flow demonstrates**:
- Spec (FR-001, FR-013, FR-014) → Command logic
- Data Model (Task schema) → Domain validation
- Storage abstraction → File persistence
- CLI contract → Output format

---

### Extensibility for Future Agents

**AI-Native Design Enablers**:
1. **Structured Data**: All tasks in JSON enable agent introspection
2. **Declarative Recurrence**: Enum-based rules allow agent reasoning
3. **Clear Commands**: Predictable CLI patterns enable agent automation
4. **Validation Rules**: Explicit constraints in data model guide agents

**Future Agent Capabilities** (not in scope, but enabled by design):
- Agent reads tasks from JSON and suggests priorities based on keywords
- Agent analyzes recurrence patterns and optimizes schedules
- Agent generates natural language summaries of task lists
- Agent suggests task breakdowns based on complexity keywords

**Preservation Strategy**:
- Keep JSON format stable (add fields, don't remove/rename)
- Keep command syntax backward compatible (add flags, don't change existing)
- Keep validation rules documented in data-model.md

---

### Refactoring Without Breaking Specs

**Allowed Refactorings**:
- Change internal implementation (e.g., switch to database storage) as long as:
  - Storage interface contract unchanged
  - Data model schema backward compatible
  - CLI command syntax unchanged
  - All acceptance tests still pass

**Forbidden Refactorings** (require spec update):
- Change Task schema in non-backward-compatible way (e.g., rename fields)
- Change CLI command syntax (e.g., rename commands, change flag names)
- Change validation rules (e.g., allow empty titles)

**Process for Breaking Changes**:
1. Update spec.md with new requirements
2. Update data-model.md with schema migration plan
3. Update contracts/cli-commands.md with new syntax
4. Implement changes
5. Update all tests to match new spec
6. Document in ADR (if architecturally significant)

---

## Documentation Update Flow

**On Implementation Start**:
1. Create `tasks.md` from this plan (via `/sp.tasks`)
2. Tasks reference spec FR numbers and contract command names

**During Implementation**:
1. Update `quickstart.md` if developer workflow changes
2. Update `data-model.md` if schema evolves
3. Update `contracts/cli-commands.md` if command syntax changes
4. Update `research.md` if new decisions made

**On Implementation Complete**:
1. Mark all tasks in `tasks.md` as complete
2. Update spec.md status from "Draft" to "Implemented"
3. Create ADR for any architecturally significant decisions made during implementation
4. Update README.md with usage examples and installation instructions

**Constitutional Compliance**:
- All documentation changes require rationale in commit messages
- Spec changes require re-validation of affected tests
- Breaking changes require explicit migration plan

---

## Risk Analysis

### Top 3 Risks

**Risk 1: File Corruption During Concurrent Access**
- **Probability**: Low (single-user CLI, no concurrent access expected)
- **Impact**: Medium (data loss)
- **Mitigation**: Atomic writes (temp file + rename), JSON validation on load, backup file on corruption
- **Kill Switch**: Detect corruption, restore from `.todo-data.json.backup`, warn user

**Risk 2: Reminder Polling Performance Degradation**
- **Probability**: Low (60-second interval is infrequent)
- **Impact**: Low (slight CPU usage)
- **Mitigation**: Optimize reminder check (filter tasks with `reminderTime != null` first), limit iteration
- **Kill Switch**: Add `--no-reminders` flag to disable polling if performance issue arises

**Risk 3: Recurrence Calculation Edge Cases (Month-End)**
- **Probability**: Medium (e.g., Jan 31 → Feb 31 doesn't exist)
- **Impact**: Low (wrong due date for recurring task)
- **Mitigation**: Use language date library for month arithmetic (handles edge cases), add explicit tests
- **Kill Switch**: Fallback to last day of month if target day doesn't exist

---

## Next Steps

1. ✅ **Planning Complete**: This document (`plan.md`) approved
2. **Task Generation**: Run `/sp.tasks` to create executable task list from this plan
3. **Implementation**: Follow task list, implement Level 1 → Level 2 → Level 3
4. **Testing**: Run acceptance tests after each level
5. **Documentation**: Update quickstart and README as needed
6. **Release**: Deploy after Level 3 gate passes

**Readiness**: Plan ready for task breakdown. Proceed to `/sp.tasks` when ready to begin implementation.

---

## References

- **Specification**: [spec.md](./spec.md)
- **Data Model**: [data-model.md](./data-model.md)
- **CLI Contracts**: [contracts/cli-commands.md](./contracts/cli-commands.md)
- **Research**: [research.md](./research.md)
- **Quickstart**: [quickstart.md](./quickstart.md)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
