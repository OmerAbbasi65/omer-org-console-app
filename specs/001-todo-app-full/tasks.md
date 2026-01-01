---
description: "Task list for AI-Native Todo Console Application implementation"
---

# Tasks: AI-Native Todo Console Application

**Input**: Design documents from `/specs/001-todo-app-full/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT included (not explicitly requested in specification)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (as per plan.md)
- Paths shown below follow language-agnostic naming (use appropriate extensions for chosen language)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan (src/, src/cli/, src/domain/, src/storage/, src/reminder/)
- [ ] T002 Initialize project with chosen language (Python/Node.js/Go/Rust) and configure dependencies (JSON parsing, CLI arg parsing, datetime)
- [ ] T003 [P] Create README.md with installation and usage instructions
- [ ] T004 [P] Configure linting and formatting tools for chosen language

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create Task entity base structure in src/domain/task with Level 1 fields (id, title, description, completed, createdAt, updatedAt)
- [ ] T006 Implement timestamp-based ID generation function in src/domain/task (format: task-<unix-timestamp-ms>)
- [ ] T007 Implement Task validation logic in src/domain/task (non-empty title, max 500 chars title, max 5000 chars description)
- [ ] T008 Create Storage interface in src/storage/storage-interface with methods (loadTasks, saveTasks, ensureStorageExists)
- [ ] T009 Implement FileStorage class in src/storage/file-storage for JSON read/write to ~/.todo-data.json
- [ ] T010 Implement atomic file writes in src/storage/file-storage (write to temp file, then rename)
- [ ] T011 Implement graceful error handling in src/storage/file-storage (create if missing, fallback to empty array if corrupted)
- [ ] T012 [P] Create CLI argument parser in src/cli/parser for command routing
- [ ] T013 [P] Create output formatter in src/cli/formatter for tabular display and success/error messages
- [ ] T014 Create main entry point in src/main that dispatches to command handlers

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Task Management (Priority: P1) 🎯 MVP

**Goal**: Deliver MVP with core task CRUD and file persistence

**Independent Test**: Create tasks via CLI, view them, mark complete/incomplete, update content, and delete them. Verify all tasks persist across app restarts.

### Implementation for User Story 1

- [ ] T015 [P] [US1] Implement add command in src/cli/commands/level1/add (parse title and optional description, create Task, save to storage)
- [ ] T016 [P] [US1] Implement list command in src/cli/commands/level1/list (load all tasks, format as table with ID/title/status)
- [ ] T017 [US1] Implement update command in src/cli/commands/level1/update (find task by ID, update title/description, save to storage)
- [ ] T018 [US1] Implement complete command in src/cli/commands/level1/complete (find task by ID, set completed=true, save to storage)
- [ ] T019 [US1] Implement incomplete command in src/cli/commands/level1/incomplete (find task by ID, set completed=false, save to storage)
- [ ] T020 [US1] Implement delete command in src/cli/commands/level1/delete (find task by ID, remove from storage)
- [ ] T021 [US1] Add error handling for all Level 1 commands (empty title, non-existent ID, storage errors)
- [ ] T022 [US1] Add input validation for all Level 1 commands per contracts/cli-commands.md

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Organization (Priority: P2)

**Goal**: Add organization and discovery capabilities with priorities, tags, search, filter, and sort

**Independent Test**: Create tasks with priorities and tags, search by keyword, filter by status/priority/tag (composable), and sort by various fields. Verify all existing tasks from US1 still work correctly.

### Implementation for User Story 2

- [ ] T023 [P] [US2] Extend Task entity in src/domain/task with Level 2 fields (priority, tags) and validation (priority enum, tag max length)
- [ ] T024 [P] [US2] Implement TaskFilter class in src/domain/task-filter for composable AND filtering (status, priority, tag, keyword)
- [ ] T025 [P] [US2] Implement case-insensitive partial keyword search in src/domain/task-filter (matches title and description)
- [ ] T026 [P] [US2] Implement TaskSort class in src/domain/task-sort for multi-field sorting (priority, title, dueDate, createdAt)
- [ ] T027 [US2] Enhance add command in src/cli/commands/level1/add to accept --priority and --tags flags
- [ ] T028 [US2] Implement set-priority command in src/cli/commands/level2/set-priority (update task priority by ID)
- [ ] T029 [US2] Implement set-tags command in src/cli/commands/level2/set-tags (update task tags by ID)
- [ ] T030 [US2] Implement search command in src/cli/commands/level2/search (call TaskFilter with keyword, display results)
- [ ] T031 [US2] Implement filter command in src/cli/commands/level2/filter (support --status, --priority, --tag with AND composition)
- [ ] T032 [US2] Implement sort command in src/cli/commands/level2/sort (support --by field and --order asc/desc, display-only no persistence per FR-023)
- [ ] T033 [US2] Add validation for Level 2 commands (priority enum values, tag lengths, empty search criteria)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Advanced Time Management (Priority: P3)

**Goal**: Add time-based intelligence with due dates, recurring tasks, and reminder notifications

**Independent Test**: Create tasks with due dates, set up recurring tasks (daily/weekly/monthly), verify auto-rescheduling on completion, and confirm reminder notifications appear at scheduled time. Verify no regressions in US1/US2.

### Implementation for User Story 3

- [ ] T034 [P] [US3] Extend Task entity in src/domain/task with Level 3 fields (dueDate, recurrence, reminderTime, lastNotified) and validation (ISO-8601 format, recurrence enum)
- [ ] T035 [P] [US3] Implement recurrence calculation functions in src/domain/recurrence (daily: +1 day, weekly: +7 days, monthly: +1 month with month-end handling)
- [ ] T036 [P] [US3] Implement overdue detection function in src/domain/task (dueDate < now AND completed == false)
- [ ] T037 [US3] Implement ReminderService in src/reminder/reminder-service with 60-second polling background thread/timer
- [ ] T038 [US3] Implement reminder check logic in src/reminder/reminder-service (reminderTime <= now AND !completed AND !notified today)
- [ ] T039 [US3] Implement console notification display in src/reminder/reminder-service (format: "🔔 REMINDER: [title] is due at [time]")
- [ ] T040 [US3] Implement lastNotified timestamp update in src/reminder/reminder-service to prevent duplicate alerts
- [ ] T041 [US3] Enhance add command in src/cli/commands/level1/add to accept --due, --recurrence, --remind flags
- [ ] T042 [US3] Enhance complete command in src/cli/commands/level1/complete to handle recurring task rescheduling (calculate next due date, reset completed=false)
- [ ] T043 [US3] Enhance list command in src/cli/commands/level1/list to show overdue indicators and recurrence info
- [ ] T044 [US3] Implement set-due command in src/cli/commands/level3/set-due (update task due date by ID, validate ISO-8601 format)
- [ ] T045 [US3] Implement set-recurrence command in src/cli/commands/level3/set-recurrence (update task recurrence pattern by ID)
- [ ] T046 [US3] Implement set-reminder command in src/cli/commands/level3/set-reminder (update task reminder time by ID, validate before due date)
- [ ] T047 [US3] Add validation for Level 3 commands (date format, recurrence enum, reminder before due date constraint)
- [ ] T048 [US3] Integrate ReminderService startup in src/main (start polling when app starts)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T049 [P] Add comprehensive error messages per contracts/cli-commands.md for all failure scenarios
- [ ] T050 [P] Verify tabular output formatting matches contracts/cli-commands.md specification
- [ ] T051 [P] Add usage help text for all commands (--help flag)
- [ ] T052 Code cleanup and refactoring for consistency across commands
- [ ] T053 Performance optimization: verify app starts in < 2 seconds (NFR-004)
- [ ] T054 Performance optimization: verify commands execute in < 3 seconds (NFR-005)
- [ ] T055 Performance optimization: test with 1,000 tasks and verify list performance (SC-005)
- [ ] T056 [P] Update README.md with complete command reference and examples
- [ ] T057 [P] Run quickstart.md validation (manual checklist verification)
- [ ] T058 Edge case handling: test all 10 edge cases from spec.md and verify graceful handling

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 → US2 → US3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Extends US1 Task entity and add command but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Extends US1/US2 Task entity and commands but independently testable

### Within Each User Story

- Tasks marked [P] can run in parallel (different files, no dependencies)
- Entity extensions before command implementations
- Core domain logic before CLI commands
- Enhanced commands depend on entity field additions
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (T012, T013 can run alongside T005-T011)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Within US1: T015, T016 can run in parallel (different files)
- Within US2: T023, T024, T025, T026 can all run in parallel (different files)
- Within US3: T034, T035, T036 can all run in parallel (different files)
- All Polish phase tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes, launch these US1 tasks in parallel:
Task T015: Implement add command in src/cli/commands/level1/add
Task T016: Implement list command in src/cli/commands/level1/list

# After T015-T016 complete, launch these in parallel:
Task T017: Implement update command in src/cli/commands/level1/update
Task T018: Implement complete command in src/cli/commands/level1/complete
Task T019: Implement incomplete command in src/cli/commands/level1/incomplete
Task T020: Implement delete command in src/cli/commands/level1/delete
```

---

## Parallel Example: User Story 2

```bash
# After Foundational phase completes, launch these US2 domain tasks in parallel:
Task T023: Extend Task entity with priority and tags
Task T024: Implement TaskFilter class
Task T025: Implement case-insensitive search
Task T026: Implement TaskSort class

# After domain logic completes, launch command implementations in parallel:
Task T028: Implement set-priority command
Task T029: Implement set-tags command
Task T030: Implement search command
Task T031: Implement filter command
Task T032: Implement sort command
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T014) - CRITICAL blocking phase
3. Complete Phase 3: User Story 1 (T015-T022)
4. **STOP and VALIDATE**: Test all US1 acceptance scenarios
   - Create task → verify ID generated and persisted
   - List tasks → verify table format correct
   - Update task → verify changes saved
   - Complete/incomplete task → verify status changes
   - Delete task → verify removal
   - Restart app → verify all tasks still present
5. Deploy/demo if ready - this is a functional MVP!

### Incremental Delivery

1. Complete Setup + Foundational (T001-T014) → Foundation ready
2. Add User Story 1 (T015-T022) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (T023-T033) → Test independently → Deploy/Demo (enhanced productivity)
4. Add User Story 3 (T034-T048) → Test independently → Deploy/Demo (full feature set)
5. Polish (T049-T058) → Final quality pass → Production release

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T014)
2. Once Foundational is done (checkpoint passed):
   - Developer A: User Story 1 (T015-T022)
   - Developer B: User Story 2 (T023-T033) - can start immediately
   - Developer C: User Story 3 (T034-T048) - can start immediately
3. Stories complete and integrate independently
4. Team collaborates on Polish phase (T049-T058)

---

## Task Summary

**Total Tasks**: 58

**By Phase**:
- Phase 1 (Setup): 4 tasks
- Phase 2 (Foundational): 10 tasks (BLOCKING)
- Phase 3 (US1 - Basic): 8 tasks
- Phase 4 (US2 - Organization): 11 tasks
- Phase 5 (US3 - Advanced): 15 tasks
- Phase 6 (Polish): 10 tasks

**By User Story**:
- User Story 1 (P1 - Basic): 8 tasks
- User Story 2 (P2 - Organization): 11 tasks
- User Story 3 (P3 - Advanced): 15 tasks
- Infrastructure (Setup + Foundational): 14 tasks
- Cross-cutting (Polish): 10 tasks

**Parallel Opportunities**: 22 tasks marked [P] can run in parallel with others

**Independent Test Criteria**:
- **US1**: Create, view, update, delete, complete/incomplete tasks; verify persistence
- **US2**: Create with priority/tags, search, filter (composable), sort; verify US1 still works
- **US3**: Due dates, recurring tasks (auto-reschedule), reminders (60s polling); verify US1/US2 still work

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (Tasks T001-T022) = 22 tasks for functional todo list

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- All tasks include exact file paths for implementation
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Validation Checklist

Before marking tasks complete, verify:

- [ ] All 58 tasks follow format: `- [ ] [ID] [P?] [Story?] Description with file path`
- [ ] All user story tasks have [US1], [US2], or [US3] label
- [ ] All foundational tasks (T005-T014) marked as blocking for user stories
- [ ] File paths specified for all implementation tasks
- [ ] Parallel tasks marked with [P] have no dependencies on incomplete tasks
- [ ] Each user story has independent test criteria defined
- [ ] MVP scope clearly identified (Setup + Foundational + US1)
- [ ] Dependency graph shows user story completion order
- [ ] Parallel execution examples provided for US1 and US2
