# ADR-002: Data Architecture and Storage Strategy

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Data Architecture" includes ID strategy, recurrence modeling, delete handling, timezone strategy).

- **Status:** Accepted
- **Date:** 2026-01-09
- **Feature:** 004-phase2-fullstack-web
- **Context:** Need to define data architecture for task management system that supports CRUD operations, recurring tasks with automatic next occurrence generation, reminders with timezone handling, and future scalability to 10,000 tasks per user and multi-tenant deployment. Must balance simplicity (Phase 2 single-user) with extensibility (future multi-user, compliance, audit trails).

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Data model affects all queries, migrations, performance
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Multiple approaches for IDs, recurrence, delete, timezone
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Affects database, API, frontend, agents, testing
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Task Identification**:
- **Primary Key**: UUID v4 (globally unique, 128-bit, standard library support)
- **Rationale**: Simplicity wins over ordering (chronological sorting uses `created_at` timestamp)
- **Rejection**: ULID (sortable UUIDs) - added complexity not justified for Phase 2 scale (10,000 tasks)

**Recurrence Modeling**:
- **Strategy**: Instance Generation on Completion
- **Implementation**: When user marks recurring task complete, Recurrence Reasoning Agent calculates next occurrence and creates new task row with same title/description but new `due_date`
- **Parent Tracking**: `parent_id` field links child occurrences to original recurring task
- **Rationale**: Simpler queries (each task is independent row), easier to modify/delete individual occurrences, matches user mental model

**Delete Handling**:
- **Strategy**: Hard Delete (permanent removal) for Phase 2
- **Implementation**: `DELETE FROM tasks WHERE id = ?` with confirmation prompt in UI
- **No Soft Delete**: No `deleted_at` field, no query filtering overhead
- **Rationale**: Simplicity for single-user system, no compliance requirements (GDPR not applicable), confirmation prompt prevents accidental deletion
- **Future Migration**: Can add `deleted_at` field in MINOR version (backward compatible) when multi-user or compliance requirements emerge

**Timezone Handling**:
- **Storage**: All timestamps stored as UTC in database (`TIMESTAMP WITH TIME ZONE`)
- **Conversion**: Frontend converts to user's local timezone for display
- **API**: All API requests/responses use ISO-8601 format with timezone (e.g., `2026-01-10T10:00:00Z`)
- **Rationale**: Single source of truth (UTC), no DST ambiguity, works for future multi-timezone support

**Indexing Strategy**:
- **Primary Index**: `id` (UUID, B-tree)
- **Query Indexes**:
  - `completed` (B-tree) - filter active/completed tasks
  - `due_date` (B-tree) - sort by due date, find overdue tasks
  - `priority` (B-tree) - filter by priority
  - `tags` (GIN index) - array search for tags
  - `created_at` (B-tree) - chronological sorting
  - `parent_id` (B-tree) - find child occurrences of recurring tasks

## Consequences

### Positive

1. **Query Performance**:
   - Instance generation enables simple queries: `SELECT * FROM tasks WHERE completed = FALSE` (no complex date arithmetic)
   - No runtime date calculations for recurring tasks (pre-generated instances)
   - Indexes optimize common queries (filter by completed, due_date, priority)
   - Expected query performance: < 500ms p95 for 10,000 tasks

2. **User Mental Model Alignment**:
   - Recurring tasks appear as distinct items in task list (not calculated views)
   - User can edit/delete individual occurrences without affecting recurrence rule
   - "Weekly standup" on Jan 10 and Jan 17 are separate tasks with independent completion status

3. **Simplicity**:
   - UUID v4 is standard library (no custom ID generation logic)
   - Hard delete has no query overhead (`WHERE deleted_at IS NULL` not needed)
   - UTC storage eliminates timezone conversion bugs in database layer

4. **Extensibility**:
   - UUID v4 supports future distributed systems (globally unique across services)
   - Instance generation scales to 50,000 total rows (10,000 tasks × 50% recurring × 10 occurrences avg = 25 MB storage)
   - Can add soft delete in MINOR version without breaking existing queries

5. **Edge Case Handling**:
   - Recurrence Reasoning Agent handles month-end dates (Jan 31 → Feb 28/29)
   - Agent handles leap years correctly (Python datetime library)
   - Timezone-aware timestamps handle DST transitions (UTC stored, local timezone applied in frontend)

### Negative

1. **Storage Overhead**:
   - UUID v4 is 16 bytes vs 4 bytes (INT) - 4x larger primary key
   - Instance generation creates more rows (52 rows for weekly task over 1 year vs 1 row for rule-based)
   - Storage cost: Acceptable at Phase 2 scale (25 MB for 50,000 rows), but may require archival strategy at 1M+ tasks

2. **Index Fragmentation**:
   - UUID v4 is non-sequential, causing B-tree index fragmentation (slight performance degradation)
   - Mitigation: PostgreSQL auto-vacuums and reindexes periodically

3. **No Undo for Deleted Tasks**:
   - Hard delete is permanent (user cannot recover accidentally deleted tasks)
   - Mitigation: UI shows confirmation prompt ("Are you sure you want to delete 'Task Title'?")
   - Future: Add soft delete when multi-user or compliance requirements emerge

4. **Data Duplication**:
   - Recurring tasks duplicate title/description across instances (e.g., "Weekly standup" stored 52 times)
   - Storage cost: Acceptable tradeoff for query performance (500 bytes/task × 52 instances = 26 KB)

5. **No Built-In Audit Trail**:
   - Hard delete means no history of deleted tasks (not suitable for compliance/audit scenarios)
   - Future: Add `deleted_at` soft delete or separate `tasks_history` table when needed

## Alternatives Considered

### Alternative A: ULID + Rule-Based Recurrence + Soft Delete + Local Timezone Storage
- **IDs**: ULID (sortable UUIDs)
- **Recurrence**: Store recurrence rule, calculate instances on-demand
- **Delete**: Flag-based soft delete (`deleted_at` timestamp)
- **Timezone**: Store local timezone timestamps

**Why Rejected**:
- ULID adds dependency and complexity without significant benefit (ordering can use `created_at`)
- Rule-based recurrence requires complex SQL date arithmetic (`generate_series()`, `date_trunc()`)
- Soft delete adds query overhead (`WHERE deleted_at IS NULL` in every query) - premature optimization for Phase 2
- Local timezone storage causes DST bugs and makes multi-timezone support harder

### Alternative B: Auto-Incrementing INT + Pre-Generate Instances + Archival Table + Mixed Timezones
- **IDs**: Auto-incrementing INT (simplest, most compact)
- **Recurrence**: Pre-generate 10 future occurrences on task creation
- **Delete**: Move to separate `tasks_archived` table
- **Timezone**: Mix of UTC and local (inconsistent)

**Why Rejected**:
- Auto-incrementing INT exposes task count (security leak) and breaks in distributed systems
- Pre-generating instances shows far-future tasks user may never complete (poor UX)
- Archival table adds cross-table query complexity
- Mixed timezone storage causes bugs and makes queries ambiguous

### Alternative C: Snowflake ID + Hybrid Recurrence + Soft Delete + UTC Storage
- **IDs**: Snowflake ID (64-bit, sortable, includes timestamp)
- **Recurrence**: Store rule + generate next 3 occurrences (hybrid)
- **Delete**: Soft delete with `deleted_at`
- **Timezone**: UTC storage (same as chosen)

**Why Rejected**:
- Snowflake ID requires custom implementation and clock synchronization (over-engineered for Phase 2)
- Hybrid recurrence adds complexity (rule storage + instance generation logic)
- Soft delete adds query overhead not justified for single-user Phase 2

## References

- Feature Spec: [specs/004-phase2-fullstack-web/sp.requirements.md](../../specs/004-phase2-fullstack-web/sp.requirements.md)
- Data Model Specification: [specs/004-phase2-fullstack-web/contracts/sp.data-model.md](../../specs/004-phase2-fullstack-web/contracts/sp.data-model.md)
- Research Decisions: [specs/004-phase2-fullstack-web/sp.research.md](../../specs/004-phase2-fullstack-web/sp.research.md) (Decisions 1, 2, 5)
- Implementation Plan: [specs/004-phase2-fullstack-web/sp.plan.md](../../specs/004-phase2-fullstack-web/sp.plan.md)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (Data Layer Requirements)
- Related ADRs: ADR-001 (Technology Stack - PostgreSQL choice), ADR-003 (AI-Native Architecture - Recurrence Reasoning Agent)
- Evaluator Evidence: N/A (architectural decision documented in planning phase)
