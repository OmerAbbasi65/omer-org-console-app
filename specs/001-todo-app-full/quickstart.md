# Quickstart Guide: AI-Native Todo Console Application

**Feature**: 001-todo-app-full
**Audience**: Developers implementing the application
**Date**: 2026-01-01

## Purpose

This guide provides a rapid-start overview for developers implementing the Todo Console Application, covering architecture, workflow, and key decision points.

## Implementation Workflow

### Phase Progression

Implement features in strict constitutional order:

1. **Level 1 - Basic** (MANDATORY, BLOCKING)
   - Add, Delete, Update, View, Complete/Incomplete
   - File-based storage
   - Basic error handling
   - **GATE**: All Level 1 acceptance tests must pass before proceeding

2. **Level 2 - Intermediate** (after Level 1 complete)
   - Priorities, Tags
   - Search, Filter, Sort
   - Enhanced CLI output
   - **GATE**: All Level 2 acceptance tests must pass + no Level 1 regressions

3. **Level 3 - Advanced** (after Level 2 complete)
   - Due dates, Recurrence, Reminders
   - Overdue indicators
   - 60-second reminder polling
   - **GATE**: All Level 3 acceptance tests must pass + no Level 1/2 regressions

---

## Architecture Overview

### Layered Architecture

```
┌─────────────────────────────────────┐
│         CLI Layer                   │  ← Commands (add, list, filter, etc.)
├─────────────────────────────────────┤
│         Domain Layer                │  ← Task, TaskFilter, TaskSort
├─────────────────────────────────────┤
│         Storage Layer               │  ← FileStorage (JSON persistence)
└─────────────────────────────────────┘
```

**CLI Layer**: Parses arguments, validates input, calls domain logic, formats output
**Domain Layer**: Business logic (task creation, filtering, recurrence calculation)
**Storage Layer**: Persistence abstraction (load/save tasks from `~/.todo-data.json`)

---

## Key Decisions (from research.md)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Task ID** | Timestamp-based (`task-<ms>`) | Unique, chronologically sortable, no counter needed |
| **Storage** | JSON file at `~/.todo-data.json` | Human-readable, simple, constitutional requirement |
| **Recurrence** | Enum + date calculation | Declarative data model, covers daily/weekly/monthly |
| **Reminders** | 60-second polling | Simple, meets "within 60s" requirement, no daemon |
| **Search** | Case-insensitive partial match | User-friendly, matches clarification |
| **CLI UX** | Verb-first commands, tabular output | Industry standard, scriptable |

---

## Project Structure (Recommended)

```
project-root/
├── src/
│   ├── cli/
│   │   ├── parser.{ext}         # Argument parsing
│   │   ├── commands/
│   │   │   ├── add.{ext}
│   │   │   ├── list.{ext}
│   │   │   ├── update.{ext}
│   │   │   ├── delete.{ext}
│   │   │   ├── complete.{ext}
│   │   │   └── ...{ext}
│   │   └── formatter.{ext}      # Output formatting (tables, messages)
│   ├── domain/
│   │   ├── task.{ext}           # Task entity + validation
│   │   ├── filter.{ext}         # TaskFilter logic
│   │   ├── sort.{ext}           # TaskSort logic
│   │   └── recurrence.{ext}     # Recurrence calculation
│   ├── storage/
│   │   ├── interface.{ext}      # Storage abstraction
│   │   └── file-storage.{ext}   # JSON file implementation
│   └── main.{ext}               # Entry point
├── tests/
│   ├── unit/                    # Unit tests per module
│   ├── integration/             # CLI command integration tests
│   └── acceptance/              # Spec acceptance scenario tests
├── specs/                       # This directory (spec, plan, data-model, etc.)
└── README.md
```

**Note**: `{ext}` = your chosen language extension (e.g., `.py`, `.js`, `.ts`, `.go`)

---

## Implementation Checklist

### Level 1 - Basic

**Data Model**:
- [ ] Implement Task entity with fields: `id`, `title`, `description`, `completed`, `createdAt`, `updatedAt`
- [ ] Implement timestamp-based ID generation
- [ ] Implement Task validation (title non-empty, max lengths)

**Storage**:
- [ ] Implement Storage interface (`loadTasks`, `saveTasks`, `ensureStorageExists`)
- [ ] Implement FileStorage with JSON read/write to `~/.todo-data.json`
- [ ] Implement atomic writes (temp file + rename)
- [ ] Handle missing/corrupted file gracefully (empty array fallback)

**Commands**:
- [ ] Implement `add <title> [--description]`
- [ ] Implement `list` (tabular output)
- [ ] Implement `update <id> [--title] [--description]`
- [ ] Implement `complete <id>`
- [ ] Implement `incomplete <id>`
- [ ] Implement `delete <id>`

**Validation**:
- [ ] Run acceptance tests for all US1 scenarios (spec.md lines 28-35)
- [ ] Verify error handling for edge cases (empty title, invalid ID, etc.)
- [ ] Confirm output matches contract format (cli-commands.md)

---

### Level 2 - Intermediate

**Data Model**:
- [ ] Add `priority`, `tags` fields to Task
- [ ] Implement priority validation (high/medium/low)
- [ ] Implement tag validation (max 50 chars)

**Domain Logic**:
- [ ] Implement TaskFilter with AND composition
- [ ] Implement case-insensitive partial search
- [ ] Implement TaskSort with priority/title/dueDate/createdAt ordering

**Commands**:
- [ ] Enhance `add` with `--priority` and `--tags`
- [ ] Implement `set-priority <id> <level>`
- [ ] Implement `set-tags <id> <tags>`
- [ ] Implement `search <keyword>`
- [ ] Implement `filter [--status] [--priority] [--tag]`
- [ ] Implement `sort --by <field> [--order]`

**Validation**:
- [ ] Run acceptance tests for all US2 scenarios (spec.md lines 47-54)
- [ ] Verify composable filters work correctly
- [ ] Confirm sorting does not mutate storage (FR-023)
- [ ] Verify no Level 1 regressions

---

### Level 3 - Advanced

**Data Model**:
- [ ] Add `dueDate`, `recurrence`, `reminderTime`, `lastNotified` to Task
- [ ] Implement ISO-8601 date validation
- [ ] Implement recurrence pattern validation

**Domain Logic**:
- [ ] Implement recurrence date calculation (daily +1 day, weekly +7 days, monthly +1 month)
- [ ] Implement recurring task reset on completion (reset `completed`, update `dueDate`)
- [ ] Implement overdue detection (`dueDate < now AND !completed`)

**Reminder System**:
- [ ] Implement 60-second polling background thread/timer
- [ ] Implement reminder check (`reminderTime <= now AND !completed AND lastNotified != today`)
- [ ] Implement console notification output
- [ ] Update `lastNotified` after notification

**Commands**:
- [ ] Enhance `add` with `--due`, `--recurrence`, `--remind`
- [ ] Implement `set-due <id> <datetime>`
- [ ] Implement `set-recurrence <id> <pattern>`
- [ ] Implement `set-reminder <id> <datetime>`
- [ ] Enhance `list` with overdue indicators and recurrence info
- [ ] Update `complete` to handle recurring task rescheduling

**Validation**:
- [ ] Run acceptance tests for all US3 scenarios (spec.md lines 66-73)
- [ ] Verify recurring tasks reschedule correctly
- [ ] Verify reminders trigger within 60 seconds
- [ ] Verify missed reminders handled gracefully
- [ ] Verify no Level 1/2 regressions

---

## Testing Strategy

### Test Levels

1. **Unit Tests**: Test individual functions/classes in isolation
   - Task validation logic
   - Recurrence calculations
   - Filter/sort logic
   - Storage operations (with mock file system)

2. **Integration Tests**: Test command end-to-end
   - Run CLI command with arguments
   - Verify storage updates
   - Verify output format

3. **Acceptance Tests**: Test spec scenarios
   - Map each "Given-When-Then" to executable test
   - Use real storage (or isolated test file)
   - Verify against success criteria (SC-001 to SC-017)

### Test Execution

```bash
# Unit tests
<test-runner> tests/unit/

# Integration tests
<test-runner> tests/integration/

# Acceptance tests
<test-runner> tests/acceptance/

# Full suite
<test-runner> tests/
```

---

## Common Pitfalls

**❌ DON'T**:
- Skip Level 1 validation before moving to Level 2
- Hardcode business logic (use declarative data where possible)
- Mutate storage on sort operations (display-only)
- Skip error messages for validation failures
- Forget to update `updatedAt` timestamp on modifications

**✅ DO**:
- Run acceptance tests after each level
- Use atomic writes for file storage
- Validate all user inputs before processing
- Follow constitutional principles (Spec-First, AI-Native, YAGNI)
- Handle edge cases explicitly (empty lists, invalid IDs, corrupted files)

---

## Next Steps

1. **Choose Implementation Language**: Python, JavaScript/TypeScript, Go, Rust, etc.
2. **Set Up Project Structure**: Create directories per recommended layout
3. **Implement Level 1**: Start with data model → storage → commands
4. **Run Level 1 Tests**: Verify all US1 acceptance scenarios pass
5. **Proceed to Level 2**: Only after Level 1 gate passed
6. **Repeat**: Level 2 → tests → Level 3 → tests

---

## References

- **Specification**: `spec.md` - Complete requirements and acceptance criteria
- **Data Model**: `data-model.md` - Task schema and validation rules
- **CLI Contracts**: `contracts/cli-commands.md` - Command syntax and examples
- **Research**: `research.md` - Decision rationale and alternatives
- **Constitution**: `.specify/memory/constitution.md` - Governing principles

---

## Support

For questions or clarifications:
1. Check specification acceptance criteria
2. Review data-model validation rules
3. Consult CLI command contracts for exact syntax
4. Refer to research.md for decision context
