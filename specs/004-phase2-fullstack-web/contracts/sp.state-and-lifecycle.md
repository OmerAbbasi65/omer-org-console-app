# State and Lifecycle: Phase 2 Todo Web Application

**Feature**: 004-phase2-fullstack-web
**Created**: 2026-01-09
**Purpose**: Define task lifecycle states, state transitions, recurring task instance lifecycle, and reminder triggering semantics.

## Task Lifecycle States

### Primary States

A task exists in one of these mutually exclusive completion states:

| State       | Description                                       | Database Representation       |
|-------------|---------------------------------------------------|-------------------------------|
| **Active**  | Task is incomplete and requires action            | `completed = FALSE`           |
| **Completed** | Task is finished and requires no further action | `completed = TRUE`            |

### Derived States (Computed from Attributes)

These states are calculated based on task attributes, not stored explicitly:

| Derived State | Definition                                                  | Query Logic                                         |
|---------------|-------------------------------------------------------------|-----------------------------------------------------|
| **Overdue**   | Task is active and due date has passed                      | `completed = FALSE AND due_date < CURRENT_TIMESTAMP`|
| **Upcoming**  | Task is active and due within next 24 hours                 | `completed = FALSE AND due_date BETWEEN NOW() AND NOW() + INTERVAL '24 hours'`|
| **Scheduled** | Task has a due date (regardless of completion)              | `due_date IS NOT NULL`                              |
| **Unscheduled** | Task has no due date                                       | `due_date IS NULL`                                  |
| **Recurring** | Task generates future occurrences when completed            | `recurrence != 'none'`                              |

### Priority Classification

Tasks are classified by priority independently of completion state:

| Priority | Description                          | Display Treatment             |
|----------|--------------------------------------|-------------------------------|
| **High** | Urgent, critical tasks               | Red indicator, sorted first   |
| **Medium** | Standard priority (default)        | Yellow/neutral, standard sort |
| **Low**  | Non-urgent, optional tasks           | Blue/grey, sorted last        |

---

## State Transitions

### Basic Transitions (Level 1)

```
[Created] ──────────────────────────> [Active]
                                          │
                                          │ User marks complete
                                          ▼
                                      [Completed]
                                          │
                                          │ User marks incomplete
                                          ▼
                                       [Active]
```

**Transition Rules**:
1. **Creation**: New task starts in `Active` state (`completed = FALSE`)
2. **Complete**: User action sets `completed = TRUE`, updates `updated_at` timestamp
3. **Uncomplete**: User action sets `completed = FALSE`, updates `updated_at` timestamp
4. **Idempotent**: Marking completed task as complete is allowed (no-op, updates `updated_at`)
5. **Reversible**: Tasks can transition between Active ↔ Completed unlimited times

### Recurring Task Transitions (Level 3)

```
[Recurring Task (Active)] ──────────> User marks complete
                                          │
                                          ├──> [Original Task (Completed)]
                                          │
                                          └──> [New Instance (Active)] with due_date = original_due_date + recurrence_offset
```

**Transition Rules**:
1. **Completion Trigger**: Marking recurring task complete generates next occurrence
2. **Instance Creation**: New task created with same attributes (title, description, priority, tags, recurrence) but fresh ID, timestamps
3. **Due Date Calculation**:
   - **Daily**: `new_due_date = original_due_date + 1 day`
   - **Weekly**: `new_due_date = original_due_date + 7 days`
   - **Monthly**: `new_due_date = original_due_date + 1 month` (handle month-end edge cases)
4. **Parent Linkage**: New instance sets `parent_id = original_task_id` (for traceability)
5. **Independence**: New instance is independent; deleting parent does NOT cascade delete
6. **Original Task**: Original task remains completed; does NOT reset to active

### Deletion Transitions

```
[Active | Completed] ──────────> User deletes ──────────> [Deleted (removed from database)]
```

**Deletion Rules**:
1. **Hard Delete**: Phase 2 uses hard deletes (record removed from database permanently)
2. **No Soft Delete**: No `deleted_at` field; deletion is immediate and irreversible
3. **Confirmation Required**: UI must prompt for confirmation before deletion
4. **Recurring Tasks**: Deleting recurring task does NOT delete child instances (they are independent)
5. **Parent Deletion**: Deleting parent of recurring instances leaves children orphaned (`parent_id` references missing record; acceptable in Phase 2)

---

## Recurring Task Instance Lifecycle

### Instance Generation Rules

1. **Trigger Event**: Recurring task completion is the only trigger for instance generation
2. **Single Instance**: Only one next occurrence is generated per completion (no bulk generation)
3. **No Missed Instances**: If user completes task late, next occurrence is calculated from original due date, not completion time
4. **Example**:
   - Task: "Weekly standup" due 2026-01-10 10:00, recurrence = weekly
   - User completes on 2026-01-12 (2 days late)
   - Next instance due: 2026-01-17 10:00 (original due date + 7 days, NOT completion date + 7 days)

### Instance Attributes

| Attribute      | Inherited from Parent? | Notes                                                                 |
|----------------|------------------------|-----------------------------------------------------------------------|
| `id`           | No                     | New UUID generated for each instance                                  |
| `title`        | Yes                    | Copied from parent task                                               |
| `description`  | Yes                    | Copied from parent task                                               |
| `completed`    | No                     | Always starts as `FALSE` (active)                                     |
| `priority`     | Yes                    | Copied from parent task                                               |
| `tags`         | Yes                    | Copied from parent task                                               |
| `due_date`     | Calculated             | Original parent `due_date` + recurrence offset                        |
| `recurrence`   | Yes                    | Copied from parent task (instances are also recurring)                |
| `parent_id`    | Set                    | References parent task's `id`                                         |
| `created_at`   | No                     | Set to current timestamp at instance creation                         |
| `updated_at`   | No                     | Set to current timestamp at instance creation                         |

### Instance Lifecycle States

Instances follow same lifecycle as regular tasks (Active → Completed, reversible).

### Instance Independence

- Each instance is a fully independent task after creation
- Modifying parent task does NOT update existing instances
- Deleting parent task does NOT delete instances
- Uncompleting a recurring task does NOT delete the generated next instance (edge case: orphaned instance remains)

---

## Soft Delete Rules (Future Consideration)

Phase 2 does NOT implement soft deletes. Future phases may add:

**Soft Delete State**: Task marked as deleted but retained in database with `deleted_at` timestamp

**Transition**:
```
[Active | Completed] ──────────> User deletes ──────────> [Soft Deleted]
                                                              │
                                                              │ Restore action
                                                              ▼
                                                           [Active]
                                                              │
                                                              │ Permanent purge (admin action)
                                                              ▼
                                                        [Hard Deleted]
```

**Rules**:
- Soft deleted tasks excluded from normal queries (`WHERE deleted_at IS NULL`)
- Restore sets `deleted_at = NULL`
- Periodic cleanup job purges soft deleted tasks older than 30 days

**Phase 2**: This is out of scope; all deletes are hard deletes.

---

## Reminder Triggering Semantics (Conceptual)

Reminders are conceptual in Phase 2; no database table for reminders.

### Reminder States

| State           | Definition                                                  | Trigger Condition                                |
|-----------------|-------------------------------------------------------------|--------------------------------------------------|
| **Pending**     | Reminder scheduled but not yet triggered                    | `current_time < reminder_time`                   |
| **Ready**       | Reminder time reached, notification should be sent          | `reminder_time <= current_time < due_date`       |
| **Sent**        | Notification sent to user (Phase 2: no persistence)         | After notification sent (future: `reminder_sent = TRUE`)|
| **Expired**     | Due date passed without reminder being sent                 | `current_time >= due_date AND reminder not sent` |
| **Cancelled**   | Task completed or deleted before reminder triggered         | `task.completed = TRUE OR task deleted`          |

### Reminder Calculation

- **Input**: `due_date` (required), `reminder_offset` (minutes before due date, e.g., 30)
- **Calculation**: `reminder_time = due_date - reminder_offset`
- **Example**: Task due 2026-01-15 14:00, reminder offset 30 minutes → reminder time 2026-01-15 13:30

### Reminder Triggering Rules

1. **One-Time Trigger**: Each reminder triggers once (no repeat notifications)
2. **Window**: Reminder triggers when `current_time >= reminder_time AND current_time < due_date`
3. **Late Reminders**: If user accesses app after reminder time but before due date, show late reminder once
4. **Missed Reminders**: If user accesses app after due date and reminder was never sent, no notification (reminder expired)
5. **Task Completion Cancels Reminder**: Completing task before reminder time cancels reminder (no notification)
6. **Task Deletion Cancels Reminder**: Deleting task cancels pending reminders

### Notification Delivery (Phase 2)

- **Preferred**: Browser notification API (requires user permission)
- **Fallback**: In-app notification banner if browser permissions denied
- **Polling**: Frontend polls `/api/v1/tasks/reminders` every 60 seconds to check for ready reminders
- **No Persistence**: Phase 2 does NOT persist "reminder sent" state (re-polling may re-trigger notification)

### Edge Cases

| Scenario                                  | Behavior                                                                 |
|-------------------------------------------|--------------------------------------------------------------------------|
| Reminder time is in the past (new task)   | Reject task creation; reminder offset must be positive                  |
| User sets reminder after due date passed  | Reject update; cannot set reminder for past due date                    |
| Multiple browser tabs open                | Each tab may trigger notification (no deduplication in Phase 2)          |
| User offline during reminder time         | Reminder triggers when user next accesses app (late reminder)            |
| Recurring task reminder                   | Each instance has its own reminder; parent reminder does NOT carry over  |

---

## State Validation Rules

### Task Creation

- `completed` must be `FALSE` (tasks cannot be created as completed)
- `recurrence` must be `'none'` if `due_date` is `NULL`
- `priority` must be one of: `high`, `medium`, `low`
- `tags` must be array with max 10 items

### Task Update

- `recurrence` can only be set to non-`'none'` value if `due_date` is not `NULL`
- Changing `recurrence` from non-`'none'` to `'none'` is allowed (stops future instance generation)
- Changing `recurrence` pattern (e.g., `daily` → `weekly`) does NOT regenerate existing instances

### Task Completion

- Marking recurring task complete triggers instance generation BEFORE marking original complete
- If instance generation fails (e.g., database error), original task completion is rolled back (atomic transaction)

### Task Deletion

- No validation required (can delete active or completed tasks)
- Deletion of recurring task does NOT validate existence of child instances

---

## State Observability

All state transitions MUST be logged for observability:

**Log Events**:
- **TaskCreated**: `{ taskId, title, priority, dueDate, recurrence, createdAt }`
- **TaskUpdated**: `{ taskId, changedFields, updatedAt }`
- **TaskCompleted**: `{ taskId, completedAt, nextInstanceId (if recurring) }`
- **TaskUncompleted**: `{ taskId, uncompletedAt }`
- **TaskDeleted**: `{ taskId, deletedAt }`
- **RecurringInstanceGenerated**: `{ parentTaskId, newInstanceId, newDueDate, generatedAt }`
- **ReminderTriggered**: `{ taskId, reminderTime, notificationMethod }`

**Log Format**: Structured JSON to stdout for centralized collection

---

## State Consistency Guarantees

1. **Atomicity**: All state transitions are atomic (single database transaction)
2. **Isolation**: Read Committed isolation level prevents dirty reads during transitions
3. **Consistency**: Foreign key constraints enforce referential integrity (`parent_id` references valid task)
4. **Durability**: Neon PostgreSQL ensures committed state transitions are durable

---

## Future State Enhancements

Phase 3 may add:
- **In Progress State**: Tasks explicitly marked as being worked on
- **Blocked State**: Tasks waiting on external dependencies
- **Archived State**: Soft delete implementation with `archived_at` timestamp
- **Reminder Sent Tracking**: Persistent `reminder_sent` boolean field
- **Batch Operations**: Bulk state transitions (e.g., complete multiple tasks)
