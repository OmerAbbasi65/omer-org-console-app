# State and Lifecycle Specification: Level 2 (Organization)

**Phase**: Phase 2 - Level 2 (Organization Features)
**Date**: 2026-01-09

## Overview

This document defines state management rules and lifecycle semantics for Level 2 (Organization) features. No state transitions or lifecycle changes from Level 1 are modified.

---

## Task State Model (Level 2)

### Task States

Tasks in Level 2 have the same two states as Level 1:

1. **Incomplete** (`completed = false`)
2. **Completed** (`completed = true`)

**No new states added in Level 2.**

### State Transitions (Unchanged from Level 1)

```
┌─────────────┐
│ Incomplete  │ ◄─────┐
└──────┬──────┘       │
       │              │
       │ toggle       │ toggle
       │              │
       ▼              │
┌─────────────┐       │
│  Completed  │ ──────┘
└─────────────┘
```

**Transition Rules** (Unchanged):
- Toggle operation flips `completed` boolean
- No restrictions based on priority or tags
- Timestamps (`updated_at`) are updated on state change

---

## Priority Lifecycle

### Priority States

A task's priority can be in one of four states:

1. **No Priority** (`priority = null`) - Default
2. **Low Priority** (`priority = "low"`)
3. **Medium Priority** (`priority = "medium"`)
4. **High Priority** (`priority = "high"`)

### Priority Transitions

```
          ┌──────────────┐
          │ No Priority  │
          │  (null)      │
          └───────┬──────┘
                  │
      ┌───────────┼───────────┐
      │           │           │
      ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│   Low    │ │  Medium  │ │   High   │
└────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │            │
     └────────────┼────────────┘
                  │
                  ▼
          ┌──────────────┐
          │ No Priority  │
          └──────────────┘
```

**Transition Rules**:
- Priority can transition to any other priority state directly (no required intermediate states)
- Setting priority to `null` removes priority
- Priority changes do NOT affect `completed` state
- Priority can be changed on completed or incomplete tasks

**Examples**:
- `null` → `high` (setting priority for the first time)
- `high` → `medium` (downgrading priority)
- `low` → `null` (removing priority)
- `medium` → `high` (upgrading priority)

### Priority Persistence

**Creation**:
- New tasks default to `priority = null` unless explicitly set

**Update**:
- Priority can be updated via `PATCH /api/v1/tasks/{id}` with `{"priority": "high"}`
- Omitting `priority` in update request leaves it unchanged
- Setting `"priority": null` removes priority

**Completion**:
- Marking task as complete does NOT change priority
- Marking task as incomplete does NOT change priority

---

## Tag Lifecycle

### Tag States

A task's tags can be in one of these states:

1. **No Tags** (`tags = []`) - Default
2. **Tagged** (`tags = ["work", "urgent", ...]`) - One or more tags

**Tags are not stateful individually** - they are simply present or absent from the array.

### Tag Operations

**Add Tags**:
- Tags can be added when creating a task
- Tags can be added to existing tasks via update
- Maximum 20 tags per task

**Remove Tags**:
- Tags can be removed by sending updated array without those tags
- Sending `tags = []` removes all tags

**Replace Tags**:
- Updating `tags` field replaces entire array (not append/remove)
- To add one tag, client must send array with all existing tags plus new tag

**Deduplication**:
- Duplicate tags are automatically removed (case-sensitive)
- Tags are trimmed of whitespace

### Tag Persistence

**Creation**:
- New tasks default to `tags = []` unless explicitly set

**Update**:
- Tags can be updated via `PATCH /api/v1/tasks/{id}` with `{"tags": ["work", "urgent"]}`
- Omitting `tags` in update request leaves them unchanged
- Setting `"tags": []` removes all tags

**Completion**:
- Marking task as complete does NOT change tags
- Marking task as incomplete does NOT change tags

**Deletion**:
- When task is deleted, tags are deleted with it (no orphaned tags in DB)

---

## Soft Delete (Not Implemented in Level 2)

**Level 2 uses hard delete** (same as Level 1):
- `DELETE /api/v1/tasks/{id}` permanently removes task from database
- No `deleted_at` field or soft delete logic

**Soft delete is deferred to future levels** if needed.

---

## Filter State (Client-Side Only)

### Filter State Model

Filters exist only in client state and URL query parameters. They do not persist across sessions.

**Filter State Shape**:

```typescript
{
  status: "completed" | "incomplete" | null,
  priority: "high" | "medium" | "low" | "none" | null,
  tags: string[],  // Empty array means no tag filter
  search: string | null
}
```

**Default State**:
```typescript
{
  status: null,     // Show all tasks (completed and incomplete)
  priority: null,   // Show all priorities
  tags: [],         // No tag filter
  search: null      // No search
}
```

### Filter Lifecycle

**Initialization**:
- On page load, filters start at default (all null/empty)
- If URL query parameters exist, initialize from URL

**Update**:
- User changes filter → state updates → refetch tasks from API
- Filter state is ephemeral (not persisted to backend)

**Clear**:
- "Clear Filters" button resets all filters to default

**Session Persistence** (Optional):
- Not required in Level 2
- If implemented, store filters in URL query parameters only

---

## Sort State (Client-Side Only)

### Sort State Model

Sort settings exist only in client state. They do not persist across sessions.

**Sort State Shape**:

```typescript
{
  by: "priority" | "title" | "createdAt" | "updatedAt",
  order: "asc" | "desc"
}
```

**Default State**:
```typescript
{
  by: "createdAt",
  order: "desc"  // Newest tasks first
}
```

### Sort Lifecycle

**Initialization**:
- On page load, sort defaults to `createdAt desc`
- If URL query parameters exist, initialize from URL

**Update**:
- User changes sort → state updates → refetch tasks from API
- Sort state is ephemeral (not persisted to backend)

**Session Persistence** (Optional):
- Not required in Level 2
- If implemented, store sort in URL query parameters only

---

## Search State (Client-Side Only)

### Search State Model

Search query exists only in client state.

**Search State Shape**:

```typescript
{
  searchTerm: string,        // User input (real-time)
  debouncedSearch: string    // Debounced value (sent to API)
}
```

**Default State**:
```typescript
{
  searchTerm: "",
  debouncedSearch: ""
}
```

### Search Lifecycle

**Initialization**:
- On page load, search is empty

**Update**:
- User types → `searchTerm` updates immediately
- After 500ms delay → `debouncedSearch` updates → refetch tasks

**Clear**:
- User clears input or clicks X → both values reset to ""

---

## Concurrent State Changes

### Multiple Users Editing Same Task

**Scenario**: User A and User B both viewing same task

1. User A changes priority from `low` to `high`
2. User B simultaneously changes priority from `low` to `medium`
3. Both users submit updates

**Behavior** (Last-Write-Wins):
- Whichever request arrives at server last wins
- No optimistic locking in Level 2
- No conflict detection or merge logic
- User who submitted first sees their change overwritten on next refresh

**Frontend Behavior**:
- After update, task displays updated value immediately
- On page refresh, latest DB value is shown

### Task Updated While User is Editing

**Scenario**: User opens edit mode, another user updates task in DB

**Behavior**:
- User's edit form shows stale values (from when edit mode opened)
- When user saves, their values overwrite DB (last-write-wins)
- No "this task was updated by another user" warning in Level 2

**Mitigation** (Future):
- Level 3+ could add `version` field for optimistic locking
- Level 3+ could add conflict detection

---

## State Consistency Rules

### Priority Consistency

**Rule**: Priority value MUST always be one of: `null`, `"high"`, `"medium"`, `"low"`

**Enforcement**:
- Database: CHECK constraint
- Backend: Pydantic validator
- Frontend: Dropdown/select with restricted options

**Violation Handling**:
- Backend rejects with 422 Unprocessable Entity
- Frontend prevents invalid values from being submitted

### Tags Consistency

**Rule 1**: Tags MUST always be an array (never null)
**Rule 2**: Tags array MUST NOT exceed 20 items
**Rule 3**: Each tag MUST NOT exceed 50 characters
**Rule 4**: Tags MUST be deduplicated

**Enforcement**:
- Database: NOT NULL constraint, JSONB array type
- Backend: Pydantic validator, deduplication logic
- Frontend: Input validation, max count check

**Violation Handling**:
- Backend rejects with 422 Unprocessable Entity
- Frontend prevents submission or shows error

### Completed State Consistency

**Rule**: `completed` MUST always be boolean (never null)

**Enforcement**:
- Database: NOT NULL constraint, BOOLEAN type
- Backend: SQLModel field default
- Frontend: Checkbox always has value (true/false)

---

## Timestamps and Lifecycle Events

### `created_at`

**Set When**: Task is created
**Updated When**: Never (immutable)
**Affected By**:
- ❌ Priority changes
- ❌ Tag changes
- ❌ Completion toggle
- ❌ Title/description updates

### `updated_at`

**Set When**: Task is created (same as `created_at` initially)
**Updated When**: Any field is modified
**Affected By**:
- ✅ Priority changes
- ✅ Tag changes (add, remove, replace)
- ✅ Completion toggle
- ✅ Title/description updates

**Update Trigger**:
- Database trigger automatically updates on any UPDATE
- Backend explicitly sets `updated_at = datetime.utcnow()`

---

## State Diagram: Task with Level 2 Fields

```
┌─────────────────────────────────────────────────────┐
│                   Task Entity                       │
├─────────────────────────────────────────────────────┤
│ State Dimensions:                                   │
│                                                     │
│ 1. Completion: [Incomplete, Completed]             │
│ 2. Priority:   [None, Low, Medium, High]           │
│ 3. Tags:       [Empty, Tagged]                     │
│                                                     │
│ Independent State Changes:                          │
│ - Completion can change without affecting priority  │
│ - Priority can change without affecting completion  │
│ - Tags can change without affecting either          │
└─────────────────────────────────────────────────────┘
```

**Example State Combinations**:

| Completed | Priority | Tags | Valid? | Example Use Case |
|-----------|----------|------|--------|------------------|
| false | null | [] | ✅ | Just created, no organization yet |
| false | high | ["work"] | ✅ | Active high-priority work task |
| true | high | ["work"] | ✅ | Completed high-priority task (still shows priority) |
| false | null | ["personal", "urgent"] | ✅ | Urgent personal task with no priority set |
| true | medium | [] | ✅ | Completed medium-priority task, no tags |

**All combinations are valid** - no restrictions based on state combinations.

---

## Validation and Invariants

### Database Invariants (Enforced)

1. `completed` is always boolean (NOT NULL)
2. `priority` is always null or in enum set (CHECK constraint)
3. `tags` is always a JSONB array (NOT NULL, defaults to `[]`)
4. `created_at` is always set and never updated
5. `updated_at` is always set and auto-updated

### Application Invariants (Enforced)

1. Tags array never exceeds 20 items
2. Individual tags never exceed 50 characters
3. Tags are deduplicated before saving
4. Whitespace is trimmed from tags
5. Empty tags are rejected

### Frontend Invariants (Enforced)

1. Priority selector only allows valid enum values + null
2. Tag input enforces max 20 tags
3. Tag input enforces max 50 chars per tag
4. Duplicate tags are prevented in UI

---

## State Recovery and Error Handling

### Optimistic Updates (Not Implemented in Level 2)

Level 2 uses **pessimistic updates**:
- User action → API call → wait for response → update UI
- No optimistic rendering of changes before API confirms

**Future Enhancement (Level 3+)**:
- Optimistic: User action → immediate UI update → API call → rollback on error

### State Rollback

**On API Error**:
- Task state remains unchanged in UI
- User sees error message
- User can retry operation

**On Network Failure**:
- Task state remains unchanged in UI
- Error message: "Unable to connect. Please try again."
- Task list shows stale data until refresh

---

## Constitutional Compliance

✅ **Level 1 Compatibility**: No changes to Level 1 state transitions
✅ **Declarative State**: All state transitions explicitly defined
✅ **No Hidden State**: All state visible in database fields
✅ **Stateless UI**: No state persisted in frontend (ephemeral session only)
✅ **Backend as Source of Truth**: All persistent state lives in database
