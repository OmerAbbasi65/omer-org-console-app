# Research: AI-Native Todo Console Application

**Feature**: 001-todo-app-full
**Date**: 2026-01-01
**Status**: Complete

## Purpose

This document consolidates research findings to resolve technical unknowns and inform architectural decisions for the Todo Console Application implementation.

## Research Areas

### 1. CLI UX Patterns for Task Management

**Research Question**: What are established patterns for console-based task management UX?

**Findings**:
- **Command Structure**: Verb-first commands (e.g., `add`, `list`, `delete`) are standard across CLI tools (git, npm, docker)
- **Flag Conventions**: Use `--long-form` for readability and `-short` for power users
- **Output Formatting**: Tabular output with clear headers and visual separators improves scannability
- **Error Messages**: Should include command that failed + reason + suggested fix (e.g., `Error: Task ID 'xyz' not found. Use 'list' to see available tasks.`)
- **Interactive vs Non-Interactive**: For console app, non-interactive (single-command execution) is more scriptable and agent-friendly

**Decision**: Adopt verb-first command structure with long-form flags, tabular output, and descriptive error messages.

**Rationale**: Aligns with CLI conventions users already know, supports scripting/automation, and follows AI-Native Design principle (structured, predictable patterns).

---

### 2. Task ID Generation Strategy

**Research Question**: What ID generation approach balances uniqueness, readability, and chronological ordering for single-user CLI?

**Options Considered**:

| Option | Pros | Cons |
|--------|------|------|
| Sequential (1, 2, 3...) | Human-friendly, short | Breaks if tasks deleted, requires tracking counter |
| UUID v4 | Globally unique, no collisions | Long (36 chars), not human-friendly, no chronological info |
| Timestamp-based (milliseconds) | Unique for single-user, chronologically sortable | Longer than sequential, but still readable |
| Short random alphanumeric | Compact, unique enough for small datasets | No chronological info, collision risk at scale |

**Decision**: Timestamp-based IDs with format `task-<unix-timestamp-ms>` (e.g., `task-1735707600000`)

**Rationale**:
- **Uniqueness**: Unix timestamp in milliseconds ensures uniqueness for single-user usage (no two tasks created in same millisecond)
- **Chronological**: Natural ordering by creation time without additional metadata
- **No External Dependencies**: Can be generated purely from system time
- **Alignment**: Matches clarification from `/sp.clarify` session

**Tradeoffs Accepted**: Slightly longer than sequential IDs, but gain chronological sorting and no counter management.

---

### 3. Storage Abstraction Approach

**Research Question**: How should we abstract storage to support file-based persistence while enabling future extensibility?

**Options Considered**:

| Option | Pros | Cons |
|--------|------|------|
| Direct file I/O in commands | Simple, no abstraction overhead | Tight coupling, hard to test, violates Single Responsibility |
| Repository pattern | Clean separation, testable, swappable implementations | May be over-engineering for single storage type |
| Simple storage interface | Minimal abstraction, easy testing, future-proof | Still requires interface design |

**Decision**: Implement minimal storage interface with file-based implementation

**Interface Contract**:
```
Storage {
  loadTasks() → Task[]
  saveTasks(tasks: Task[]) → void
  ensureStorageExists() → void
}
```

**Rationale**:
- **Testability**: Commands can be tested with in-memory mock storage
- **Future Extensibility**: Could swap to database, cloud, or other backends without changing command layer
- **Simplicity**: Single interface with 3 methods is minimal yet sufficient
- **Constitutional Alignment**: Follows "Storage abstraction required" (Principle V)

**Implementation Details**:
- File location: `~/.todo-data.json` (user home directory, hidden file)
- Format: Pretty-printed JSON for human readability (per NFR-006)
- Atomic writes: Write to temp file + rename to prevent corruption
- Error handling: Create file if missing, validate JSON on load, fallback to empty array if corrupted

---

### 4. Recurrence Modeling Approach

**Research Question**: How should recurring tasks be modeled to support daily/weekly/monthly patterns declaratively?

**Options Considered**:

| Option | Pros | Cons |
|--------|------|------|
| Enum + hardcoded logic | Simple, predictable | Not extensible, violates "declarative" principle |
| Cron-like expressions | Very flexible, industry standard | Complex to parse, overkill for 3 simple patterns |
| Rule-based with interval field | Declarative, extensible | Requires more complex data model |

**Decision**: Enum-based with declarative data model + date calculation functions

**Data Model**:
```json
{
  "recurrence": "none" | "daily" | "weekly" | "monthly",
  "dueDate": "ISO-8601 datetime"
}
```

**Behavior**: When task is completed:
1. If `recurrence != "none"`, calculate next due date based on current `dueDate`:
   - **daily**: Add 1 day
   - **weekly**: Add 7 days
   - **monthly**: Add 1 month (same day, handle month-end edge cases)
2. Reset `completed` to `false`
3. Update `updatedTimestamp`

**Rationale**:
- **Declarative**: Recurrence pattern stored as data, not code
- **Simplicity**: Covers stated requirements (daily/weekly/monthly) without over-engineering
- **Predictable**: Clear calculation rules for each pattern
- **Edge Case Handling**: Month-end dates (e.g., Jan 31 → Feb 28/29) handled by date library

**Tradeoffs Accepted**: Limited to 3 patterns initially, but extensible by adding more enum values later.

---

### 5. Reminder Triggering Mechanism

**Research Question**: How should reminders be triggered in a foreground console application?

**Options Considered**:

| Option | Pros | Cons |
|--------|------|------|
| Polling (check periodically) | Simple, no background daemon | Uses CPU even when no reminders due |
| Event-driven (timer callbacks) | Efficient, responsive | More complex, requires event loop |
| On-command check (check during list/add) | Zero overhead when idle | Reminders only trigger on user action |

**Decision**: Polling with 60-second interval (from `/sp.clarify`)

**Implementation Approach**:
- Background thread/timer that wakes every 60 seconds
- Check all tasks for `reminderTime <= currentTime` and `completed == false`
- Display console notification for each due reminder
- Mark reminder as "notified" to avoid repeated alerts (add `lastNotified` field)

**Rationale**:
- **Simplicity**: Straightforward to implement without complex event systems
- **Acceptable Overhead**: 60-second interval is infrequent enough to be negligible
- **User Expectation**: SC-014 states "within 60 seconds" tolerance - this meets requirement
- **Graceful Degradation**: If app closed, reminders simply don't fire (per FR-032: handle missed reminders gracefully)

**Additional Considerations**:
- Notification format: Simple console output with clear visual marker (e.g., `🔔 REMINDER: [task title] is due at [time]`)
- Persistence: Don't persist notification state - re-check on app restart

---

### 6. Console Limitations & Offline Constraints

**Research Question**: What constraints does console-only, offline-first impose on design?

**Findings**:
- **No Rich UI**: Cannot use colors, icons, or interactive elements in all environments (Windows cmd vs Unix terminal)
- **Text-Only Output**: Must rely on clear formatting (spacing, separators, capitalization) for visual hierarchy
- **No Background Process**: Cannot run as daemon - reminders only work while app is running (acceptable per assumptions)
- **File System Only**: No network, no cloud - all data local
- **Cross-Platform Paths**: Must handle `~` expansion and path separators correctly (Windows `\` vs Unix `/`)

**Design Implications**:
1. Use ASCII-art tables with clear borders for list output
2. Use ALL CAPS or `===` separators for section headers
3. Assume basic terminal capabilities only (no color unless explicitly configured)
4. Implement cross-platform path resolution for `~/.todo-data.json`
5. Document "app must be running for reminders" clearly in user docs

---

## Summary

All technical unknowns have been resolved with explicit decisions documented. Key takeaways:

1. **ID Strategy**: Timestamp-based (`task-<ms>`)
2. **Storage**: Minimal interface + JSON file implementation
3. **Recurrence**: Enum-based declarative model with date calculation
4. **Reminders**: 60-second polling with console output
5. **CLI UX**: Verb-first commands, tabular output, descriptive errors
6. **Constraints**: Text-only, no background daemon, cross-platform paths

These decisions inform the architectural design in `plan.md` and data model in `data-model.md`.
