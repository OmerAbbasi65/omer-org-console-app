# CLI Command Contracts: AI-Native Todo Console Application

**Feature**: 001-todo-app-full
**Date**: 2026-01-01
**Status**: Approved

## Overview

This document defines the complete command-line interface contract for the Todo application across all three feature levels (Basic, Intermediate, Advanced).

**General Command Format**:
```
todo <command> [arguments] [options]
```

**Global Conventions**:
- Commands are case-sensitive (lowercase)
- Long-form options use `--option-name`
- Short-form options use `-o`
- String arguments with spaces must be quoted
- Exit codes: 0 (success), 1 (user error), 2 (system error)

---

## Level 1: Basic Commands

### `add` - Create New Task

**Syntax**:
```
todo add <title> [--description <text>]
```

**Arguments**:
- `<title>` (required): Task title, string, max 500 characters

**Options**:
- `--description <text>`, `-d <text>`: Extended description, string, max 5000 characters

**Examples**:
```bash
todo add "Buy groceries"
todo add "Deploy application" --description "Deploy to production environment after testing"
todo add "Fix bug #42" -d "Memory leak in task scheduler"
```

**Success Output**:
```
✓ Task created: task-1735707600000
  Title: Buy groceries
```

**Error Cases**:
| Error | Exit Code | Output |
|-------|-----------|--------|
| Empty title | 1 | `Error: Task title cannot be empty` |
| Title too long | 1 | `Error: Title exceeds 500 characters (current: 523)` |
| Description too long | 1 | `Error: Description exceeds 5000 characters (current: 5124)` |

---

### `list` - View All Tasks

**Syntax**:
```
todo list
```

**Arguments**: None

**Options**: None (Level 1 basic), sorting/filtering added in Level 2/3

**Success Output** (example):
```
ID                   | TITLE              | STATUS
---------------------|--------------------|-----------
task-1735707600000   | Buy groceries      | Incomplete
task-1735707601000   | Deploy app         | Complete
task-1735707602000   | Fix bug #42        | Incomplete

Total: 3 tasks (1 complete, 2 incomplete)
```

**Empty State Output**:
```
No tasks found.

Use 'todo add "Task title"' to create your first task.
```

---

### `update` - Modify Task Title/Description

**Syntax**:
```
todo update <task-id> [--title <new-title>] [--description <new-description>]
```

**Arguments**:
- `<task-id>` (required): Task identifier (e.g., `task-1735707600000`)

**Options** (at least one required):
- `--title <text>`, `-t <text>`: New title
- `--description <text>`, `-d <text>`: New description
- `--description ""`: Clear description (set to null)

**Examples**:
```bash
todo update task-1735707600000 --title "Buy groceries and cook dinner"
todo update task-1735707600000 -t "Buy groceries" -d "Milk, eggs, bread"
todo update task-1735707600000 --description ""
```

**Success Output**:
```
✓ Task updated: task-1735707600000
```

**Error Cases**:
| Error | Exit Code | Output |
|-------|-----------|--------|
| Task not found | 1 | `Error: Task 'task-xyz' not found. Use 'list' to see available tasks.` |
| No options provided | 1 | `Error: At least one of --title or --description required` |
| Validation error | 1 | `Error: Title cannot be empty` |

---

### `complete` - Mark Task as Complete

**Syntax**:
```
todo complete <task-id>
```

**Arguments**:
- `<task-id>` (required): Task identifier

**Examples**:
```bash
todo complete task-1735707600000
```

**Success Output**:
```
✓ Task completed: task-1735707600000
  Title: Buy groceries
```

**Note**: For recurring tasks (Level 3), this triggers rescheduling instead of marking complete.

**Error Cases**:
| Error | Exit Code | Output |
|-------|-----------|--------|
| Task not found | 1 | `Error: Task 'task-xyz' not found` |
| Already complete | 0 | `Task 'task-1735707600000' is already complete` (warning, not error) |

---

### `incomplete` - Mark Task as Incomplete

**Syntax**:
```
todo incomplete <task-id>
```

**Arguments**:
- `<task-id>` (required): Task identifier

**Examples**:
```bash
todo incomplete task-1735707600000
```

**Success Output**:
```
✓ Task marked incomplete: task-1735707600000
  Title: Buy groceries
```

**Error Cases**:
| Error | Exit Code | Output |
|-------|-----------|--------|
| Task not found | 1 | `Error: Task 'task-xyz' not found` |
| Already incomplete | 0 | `Task 'task-1735707600000' is already incomplete` (warning, not error) |

---

### `delete` - Remove Task

**Syntax**:
```
todo delete <task-id>
```

**Arguments**:
- `<task-id>` (required): Task identifier

**Examples**:
```bash
todo delete task-1735707600000
```

**Success Output**:
```
✓ Task deleted: task-1735707600000
  Title: Buy groceries
```

**Error Cases**:
| Error | Exit Code | Output |
|-------|-----------|--------|
| Task not found | 1 | `Error: Task 'task-xyz' not found` |

---

## Level 2: Intermediate Commands

### `add` (Enhanced) - Create with Priority and Tags

**Syntax** (extended from Level 1):
```
todo add <title> [--description <text>] [--priority <level>] [--tags <tag1,tag2,...>]
```

**New Options**:
- `--priority <level>`, `-p <level>`: Priority level (`high`, `medium`, or `low`)
- `--tags <tag1,tag2,...>`, `-t <tag1,tag2,...>`: Comma-separated tags

**Examples**:
```bash
todo add "Deploy app" --priority high --tags work,urgent
todo add "Buy groceries" -p low -t personal,shopping
```

**Success Output**:
```
✓ Task created: task-1735707600000
  Title: Deploy app
  Priority: high
  Tags: work, urgent
```

**Error Cases**:
| Error | Exit Code | Output |
|-------|-----------|--------|
| Invalid priority | 1 | `Error: Priority must be 'high', 'medium', or 'low' (got: 'critical')` |
| Tag too long | 1 | `Error: Tag exceeds 50 characters: 'very-long-tag-name...'` |

---

### `set-priority` - Modify Task Priority

**Syntax**:
```
todo set-priority <task-id> <level>
```

**Arguments**:
- `<task-id>` (required): Task identifier
- `<level>` (required): `high`, `medium`, `low`, or `none` (to clear)

**Examples**:
```bash
todo set-priority task-1735707600000 high
todo set-priority task-1735707600000 none
```

**Success Output**:
```
✓ Priority updated: task-1735707600000
  Priority: high
```

---

### `set-tags` - Modify Task Tags

**Syntax**:
```
todo set-tags <task-id> <tag1,tag2,...>
```

**Arguments**:
- `<task-id>` (required): Task identifier
- `<tags>` (required): Comma-separated tags, or empty string to clear

**Examples**:
```bash
todo set-tags task-1735707600000 work,urgent
todo set-tags task-1735707600000 ""
```

**Success Output**:
```
✓ Tags updated: task-1735707600000
  Tags: work, urgent
```

---

### `search` - Find Tasks by Keyword

**Syntax**:
```
todo search <keyword>
```

**Arguments**:
- `<keyword>` (required): Search term (case-insensitive, partial match)

**Examples**:
```bash
todo search "groceries"
todo search "deploy"
```

**Success Output**:
```
ID                   | TITLE              | STATUS
---------------------|--------------------|-----------
task-1735707600000   | Buy groceries      | Incomplete
task-1735707602000   | Buy groceries today| Complete

Found 2 tasks matching "groceries"
```

**Empty Result**:
```
No tasks found matching "xyz"
```

---

### `filter` - Filter Tasks by Criteria

**Syntax**:
```
todo filter [--status <complete|incomplete>] [--priority <level>] [--tag <tag>]
```

**Options** (at least one required):
- `--status <value>`: Filter by completion status
- `--priority <level>`: Filter by priority (`high`, `medium`, `low`)
- `--tag <tag>`: Filter by tag (exact match)

**Filters are composable** (AND logic).

**Examples**:
```bash
todo filter --status incomplete
todo filter --priority high
todo filter --tag work
todo filter --priority high --status incomplete
todo filter --tag work --status complete
```

**Success Output**:
```
ID                   | TITLE              | PRIORITY | STATUS
---------------------|--------------------|-----------|-----------
task-1735707600000   | Deploy app         | high      | Incomplete
task-1735707601000   | Fix production bug | high      | Incomplete

Found 2 tasks (filters: priority=high, status=incomplete)
```

---

### `sort` - Sort Task List

**Syntax**:
```
todo sort --by <field> [--order <asc|desc>]
```

**Options**:
- `--by <field>` (required): Sort field (`priority`, `title`, `due-date`, `created-at`)
- `--order <direction>`: Sort direction (`asc` or `desc`, default: field-dependent)

**Default Ordering**:
- `priority`: desc (high → medium → low → none)
- `title`: asc (A → Z)
- `due-date`: asc (earliest first)
- `created-at`: asc (oldest first)

**Examples**:
```bash
todo sort --by priority
todo sort --by title --order desc
todo sort --by due-date
```

**Success Output**: (same format as `list`, but sorted)

**Note**: Sorting does NOT persist - it's display-only per FR-023.

---

## Level 3: Advanced Commands

### `add` (Enhanced) - Create with Due Date and Recurrence

**Syntax** (extended from Level 2):
```
todo add <title> [...] [--due <datetime>] [--recurrence <pattern>] [--remind <datetime>]
```

**New Options**:
- `--due <datetime>`: Due date/time in ISO-8601 format (e.g., `2026-01-15T17:00:00`)
- `--recurrence <pattern>`: Recurrence pattern (`daily`, `weekly`, `monthly`)
- `--remind <datetime>`: Reminder time in ISO-8601 format

**Examples**:
```bash
todo add "Submit report" --due 2026-01-15T17:00:00
todo add "Daily standup" --due 2026-01-02T09:00:00 --recurrence daily
todo add "Review PR" --due 2026-01-05T14:00:00 --remind 2026-01-05T13:45:00
```

**Success Output**:
```
✓ Task created: task-1735707600000
  Title: Submit report
  Due: 2026-01-15 17:00:00
  Reminder: 2026-01-15 16:45:00
```

**Error Cases**:
| Error | Exit Code | Output |
|-------|-----------|--------|
| Invalid date format | 1 | `Error: Invalid date format. Use ISO-8601 (YYYY-MM-DDTHH:MM:SS)` |
| Recurrence without due date | 1 | `Error: Recurrence requires --due to be set` |
| Reminder without due date | 1 | `Error: Reminder requires --due to be set` |
| Reminder after due date | 1 | `Error: Reminder time must be before due date` |
| Invalid recurrence | 1 | `Error: Recurrence must be 'daily', 'weekly', or 'monthly' (got: 'hourly')` |

---

### `set-due` - Set Task Due Date

**Syntax**:
```
todo set-due <task-id> <datetime>
```

**Arguments**:
- `<task-id>` (required): Task identifier
- `<datetime>` (required): ISO-8601 datetime, or `none` to clear

**Examples**:
```bash
todo set-due task-1735707600000 2026-01-15T17:00:00
todo set-due task-1735707600000 none
```

---

### `set-recurrence` - Set Task Recurrence

**Syntax**:
```
todo set-recurrence <task-id> <pattern>
```

**Arguments**:
- `<task-id>` (required): Task identifier
- `<pattern>` (required): `daily`, `weekly`, `monthly`, or `none`

**Examples**:
```bash
todo set-recurrence task-1735707600000 daily
todo set-recurrence task-1735707600000 none
```

---

### `set-reminder` - Set Task Reminder

**Syntax**:
```
todo set-reminder <task-id> <datetime>
```

**Arguments**:
- `<task-id>` (required): Task identifier
- `<datetime>` (required): ISO-8601 datetime, or `none` to clear

**Examples**:
```bash
todo set-reminder task-1735707600000 2026-01-15T16:45:00
todo set-reminder task-1735707600000 none
```

---

### `list` (Enhanced) - Show Overdue Indicators

**Enhanced Output** (Level 3):
```
ID                   | TITLE              | DUE              | STATUS
---------------------|--------------------|-----------------|-----------
task-1735707600000   | Submit report      | 2026-01-15 17:00| OVERDUE ⚠
task-1735707601000   | Review PR          | 2026-01-20 14:00| Incomplete
task-1735707602000   | Daily standup      | 2026-01-02 09:00| Incomplete (recurring: daily)

Total: 3 tasks (0 complete, 3 incomplete, 1 overdue)
```

**Overdue Definition**: `dueDate < currentTime AND completed == false`

---

## Error Handling Standards

**All Commands**:
1. Validate arguments before execution
2. Return descriptive error messages with context
3. Suggest corrective action when possible
4. Use consistent error format: `Error: <message>`
5. Exit with code 1 for user errors, 2 for system errors

**Common System Errors**:
| Error | Exit Code | Output |
|-------|-----------|--------|
| Storage file corrupted | 2 | `Error: Task storage is corrupted. Backup found at ~/.todo-data.json.backup` |
| Storage file permission denied | 2 | `Error: Cannot access task storage. Check permissions for ~/.todo-data.json` |
| Disk full | 2 | `Error: Cannot save tasks. Disk is full.` |

---

## Output Format Standards

**Table Format** (for `list`, `filter`, `search`, `sort`):
- Column headers in ALL CAPS
- Pipe `|` separators with padding
- Horizontal lines using `-` characters
- Right-align numeric/status columns
- Truncate long fields with `...`

**Success Messages**:
- Start with `✓` (checkmark)
- Include affected task ID and relevant details
- Concise, one line when possible

**Error Messages**:
- Start with `Error:`
- Include specific failure reason
- Suggest fix or next action

---

## Alignment with Specification

- **FR-001 to FR-012**: Level 1 commands (add, list, update, complete, incomplete, delete)
- **FR-013 to FR-024**: Level 2 commands (priority, tags, search, filter, sort)
- **FR-025 to FR-035**: Level 3 commands (due dates, recurrence, reminders)
- **NFR-007**: Consistent command syntax across all operations
- **NFR-008**: All user inputs validated before processing
- **Clarifications**: Matches decisions from `/sp.clarify` session
