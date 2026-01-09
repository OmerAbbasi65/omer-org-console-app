# Feature Requirements: Todo Web Application - Level 2 (Organization)

**Feature Branch**: `003-todo-web-app-level2`
**Phase**: Phase 2 - Full-Stack Web Application
**Level**: Level 2 - Organization Features
**Created**: 2026-01-09
**Status**: Specification
**Depends On**: Level 1 (Core) - 002-todo-web-app-level1

## Constitutional Alignment

This specification strictly follows `/sp.constitution` Phase 2 rules:

1. **Progressive Feature Maturity**: Level 2 builds on Level 1 without breaking it
2. **Spec-First Development**: No code until all specs are complete
3. **Full-Stack Design**: Frontend and backend designed together
4. **Schema Evolution**: Additive-only database changes
5. **No Feature Skipping**: Level 1 must be complete before Level 2

## Level 2 Scope

**In Scope** (Organization Features):
- Task priorities (high, medium, low, none)
- Task tags (multiple tags per task)
- Search tasks by keyword
- Filter tasks by status, priority, tags
- Sort tasks by multiple fields
- Composable filters (AND logic)

**Out of Scope** (Deferred to Level 3):
- Due dates
- Recurring tasks
- Reminders
- Time-based features

## User Stories

### User Story 1 - Task Priorities (Priority: P2)

**As a user**, I want to assign priority levels to tasks so that I can focus on the most important work first.

**Why this priority**: Once users have basic task management (Level 1), they need to organize growing task lists by importance. Priorities are foundational for any productivity system.

**Acceptance Criteria**:

1. **Given** I am creating a new task, **When** I select priority "high", **Then** the task is created with priority "high"
2. **Given** a task exists, **When** I change its priority from "medium" to "high", **Then** the priority is updated immediately
3. **Given** tasks have different priorities, **When** I view the task list, **Then** I can visually distinguish priorities (colors or badges)
4. **Given** a task has no priority set, **When** I view it, **Then** it displays as "No priority" or equivalent indicator
5. **Given** I create a task without selecting priority, **When** the task is created, **Then** priority defaults to null (no priority)

**Independent Test**: Can be tested by creating tasks with different priorities, updating priorities, and verifying visual distinction and persistence.

---

### User Story 2 - Task Tags (Priority: P2)

**As a user**, I want to add multiple tags to tasks so that I can categorize them by project, context, or theme.

**Why this priority**: Tags provide flexible categorization beyond single-dimension priority. Essential for users managing tasks across multiple projects or contexts.

**Acceptance Criteria**:

1. **Given** I am creating a task, **When** I add tags "work" and "urgent", **Then** the task is created with both tags
2. **Given** a task exists, **When** I add tag "meeting" to existing tags, **Then** the new tag is appended without removing old tags
3. **Given** a task has tags, **When** I remove tag "urgent", **Then** only that tag is removed
4. **Given** a task has no tags, **When** I view it, **Then** no tags are displayed
5. **Given** I enter duplicate tags (e.g., "work, work"), **When** the task is saved, **Then** duplicate tags are deduplicated automatically
6. **Given** tasks have various tags, **When** I view the list, **Then** tags are displayed as inline badges or chips

**Independent Test**: Can be tested by adding/removing tags, verifying deduplication, and checking persistence.

---

### User Story 3 - Search Tasks (Priority: P2)

**As a user**, I want to search tasks by keyword so that I can quickly find specific items in large lists.

**Why this priority**: Search becomes critical when users have 10+ tasks. Enables fast retrieval without scrolling.

**Acceptance Criteria**:

1. **Given** I have 20 tasks, **When** I search for "groceries", **Then** only tasks with "groceries" in title or description are displayed
2. **Given** I search for "URGENT" (uppercase), **When** results are returned, **Then** search is case-insensitive (matches "urgent", "Urgent", "URGENT")
3. **Given** I search for "buy gro" (partial keyword), **When** results are returned, **Then** partial matches are included (e.g., "Buy groceries")
4. **Given** no tasks match my search term, **When** I search, **Then** I see message "No tasks found for '[search term]'"
5. **Given** I search and then clear the search box, **When** the search is cleared, **Then** all tasks are displayed again
6. **Given** a task has description "Milk, eggs, bread", **When** I search for "eggs", **Then** the task is found (description is searched)

**Independent Test**: Can be tested with various search terms, case variations, and partial matches.

---

### User Story 4 - Filter Tasks (Priority: P2)

**As a user**, I want to filter tasks by status, priority, and tags so that I can focus on specific subsets of my work.

**Why this priority**: Filtering enables focused workflows (e.g., "show only high-priority incomplete tasks"). Essential for managing 20+ tasks.

**Acceptance Criteria**:

1. **Given** I select filter "Status: Incomplete", **When** applied, **Then** only incomplete tasks are displayed
2. **Given** I select filter "Priority: High", **When** applied, **Then** only high-priority tasks are displayed
3. **Given** I select filter "Tag: work", **When** applied, **Then** only tasks with "work" tag are displayed
4. **Given** I apply multiple filters (Status: Incomplete AND Priority: High), **When** applied, **Then** only tasks matching ALL criteria are displayed (AND logic)
5. **Given** I apply filter "Tag: work AND Tag: urgent", **When** applied, **Then** only tasks with BOTH tags are displayed
6. **Given** no tasks match the applied filters, **When** I view the list, **Then** I see message "No tasks match the selected filters"
7. **Given** filters are applied, **When** I click "Clear Filters", **Then** all filters are removed and all tasks are displayed

**Independent Test**: Can be tested by applying single and composite filters, verifying AND logic, and clearing filters.

---

### User Story 5 - Sort Tasks (Priority: P2)

**As a user**, I want to sort tasks by priority, title, due date (if exists), or creation date so that I can view them in my preferred order.

**Why this priority**: Sorting provides customizable organization beyond default order. Users need different views for different workflows.

**Acceptance Criteria**:

1. **Given** I select sort "Priority (High to Low)", **When** applied, **Then** tasks are ordered: high → medium → low → no priority
2. **Given** I select sort "Title (A-Z)", **When** applied, **Then** tasks are alphabetically ordered by title
3. **Given** I select sort "Created Date (Newest First)", **When** applied, **Then** newest tasks appear at the top
4. **Given** I select sort "Created Date (Oldest First)", **When** applied, **Then** oldest tasks appear at the top
5. **Given** sorting is applied, **When** I change to a different sort option, **Then** the previous sort is replaced
6. **Given** I sort tasks, **When** I refresh the page, **Then** sorting preference is NOT persisted (resets to default)
7. **Given** tasks have no priority, **When** I sort by priority, **Then** no-priority tasks appear last

**Independent Test**: Can be tested by applying different sort options and verifying correct ordering.

---

## Functional Requirements

### Task Entity Extensions (Level 2)

- **FR-L2-001**: System MUST add `priority` field to Task entity
  - Type: String (enum)
  - Allowed values: "high", "medium", "low", null
  - Default: null (no priority)
  - Nullable: Yes

- **FR-L2-002**: System MUST add `tags` field to Task entity
  - Type: Array of strings
  - Default: Empty array `[]`
  - Nullable: No (use empty array, not null)
  - Max tags per task: 20
  - Max tag length: 50 characters per tag

### Priority Management

- **FR-L2-003**: System MUST allow users to set priority when creating a task
- **FR-L2-004**: System MUST allow users to update priority on existing tasks
- **FR-L2-005**: System MUST validate priority values against allowed set ("high", "medium", "low", null)
- **FR-L2-006**: System MUST display priority visually in UI (color coding or badges)
- **FR-L2-007**: System MUST allow removing priority (setting to null)

### Tag Management

- **FR-L2-008**: System MUST allow users to add multiple tags when creating a task
- **FR-L2-009**: System MUST allow users to add tags to existing tasks
- **FR-L2-010**: System MUST allow users to remove individual tags from tasks
- **FR-L2-011**: System MUST deduplicate tags automatically (case-sensitive: "Work" ≠ "work")
- **FR-L2-012**: System MUST trim whitespace from tag names
- **FR-L2-013**: System MUST reject tags exceeding 50 characters
- **FR-L2-014**: System MUST reject tasks with more than 20 tags
- **FR-L2-015**: System MUST display tags as inline badges in UI

### Search

- **FR-L2-016**: System MUST allow users to search tasks by keyword
- **FR-L2-017**: System MUST perform case-insensitive partial matching in title and description
- **FR-L2-018**: System MUST return results within 2 seconds for 1000 tasks
- **FR-L2-019**: System MUST display "No tasks found" message when search returns zero results
- **FR-L2-020**: System MUST clear search when search input is cleared

### Filtering

- **FR-L2-021**: System MUST allow filtering by completion status (completed/incomplete)
- **FR-L2-022**: System MUST allow filtering by priority (high/medium/low/none)
- **FR-L2-023**: System MUST allow filtering by tag (any matching tag)
- **FR-L2-024**: System MUST support composite filters with AND logic (all conditions must match)
- **FR-L2-025**: System MUST allow filtering by multiple tags (task must have ALL selected tags)
- **FR-L2-026**: System MUST provide "Clear Filters" action to reset all filters
- **FR-L2-027**: System MUST display "No tasks match filters" message when filters return zero results

### Sorting

- **FR-L2-028**: System MUST allow sorting by priority (high → medium → low → none)
- **FR-L2-029**: System MUST allow sorting by title (alphabetical A-Z or Z-A)
- **FR-L2-030**: System MUST allow sorting by creation date (newest/oldest first)
- **FR-L2-031**: System MUST NOT persist sort preference across page refreshes (session-only)
- **FR-L2-032**: System MUST default to "Created Date (Newest First)" sort order

### Backend Requirements

- **FR-L2-033**: Backend MUST validate priority enum values
- **FR-L2-034**: Backend MUST validate tag array constraints (max 20 tags, max 50 chars each)
- **FR-L2-035**: Backend MUST perform server-side search (not client-side filtering)
- **FR-L2-036**: Backend MUST support query parameters for filtering and sorting
- **FR-L2-037**: Backend MUST return filtered/sorted results in single query (no pagination in Level 2)

### Frontend Requirements

- **FR-L2-038**: Frontend MUST provide UI controls for setting priority (dropdown or buttons)
- **FR-L2-039**: Frontend MUST provide tag input component (comma-separated or chip input)
- **FR-L2-040**: Frontend MUST provide search input with debounce (500ms)
- **FR-L2-041**: Frontend MUST provide filter panel or controls
- **FR-L2-042**: Frontend MUST provide sort dropdown or buttons
- **FR-L2-043**: Frontend MUST update URL query parameters when filters/search/sort are applied (Level 2 optional, Level 3 required)

## Success Criteria

### Measurable Outcomes

- **SC-L2-001**: Users can assign priority to a task in under 5 seconds (3 clicks max)
- **SC-L2-002**: Users can add tags to a task in under 10 seconds
- **SC-L2-003**: Search returns results within 2 seconds for 1000 tasks
- **SC-L2-004**: Filters apply within 1 second for 1000 tasks
- **SC-L2-005**: Sorting completes within 500ms for 1000 tasks
- **SC-L2-006**: Composite filters (3+ conditions) work correctly 100% of the time
- **SC-L2-007**: Tag deduplication works correctly 100% of the time

### Non-Functional Requirements

- **NFR-L2-001**: Backend API responses MUST complete in under 300ms (p95) for search/filter/sort operations
- **NFR-L2-002**: Frontend MUST debounce search input to avoid excessive API calls
- **NFR-L2-003**: Priority colors MUST meet WCAG AA contrast ratio (4.5:1)
- **NFR-L2-004**: Tag badges MUST be readable and distinguishable
- **NFR-L2-005**: Database indexes MUST be added for priority and tags fields

## Constraints

- No pagination in Level 2 (all tasks returned, filtered/sorted)
- No saved filter presets (each session starts with no filters)
- No bulk tag operations (e.g., "add tag to all selected tasks")
- No tag autocomplete or suggestions in Level 2
- No priority inheritance or propagation
- Search syntax is simple keyword matching (no boolean operators like AND/OR)

## Out of Scope (Level 2)

- Due dates (Level 3)
- Recurring tasks (Level 3)
- Reminders (Level 3)
- Task dependencies
- Subtasks
- Custom priority levels
- Tag hierarchies or nested tags
- Advanced search (boolean, regex, field-specific)
- Saved searches or filters
- Export/import with priorities and tags
- Analytics or reports

## Edge Cases

### Priority Edge Cases
- What happens when a user selects an invalid priority value via API manipulation?
- What happens when sorting by priority and all tasks have null priority?
- What happens when a task's priority is updated while another user is viewing it?

### Tag Edge Cases
- What happens when a user tries to add a 21st tag?
- What happens when a tag contains only whitespace?
- What happens when a tag exceeds 50 characters?
- What happens when filtering by a tag that no longer exists on any task?
- What happens when a user enters tags with leading/trailing whitespace?
- What happens when tags contain special characters (emoji, unicode)?

### Search Edge Cases
- What happens when search term matches both title and description?
- What happens when search term is very long (>500 chars)?
- What happens when search term contains special regex characters?
- What happens when search is performed on an empty task list?

### Filter Edge Cases
- What happens when composite filters result in zero matches?
- What happens when filtering by priority "none" (null values)?
- What happens when filtering by multiple tags that no task has together?

### Sort Edge Cases
- What happens when sorting by a field that some tasks don't have (null values)?
- What happens when two tasks have identical values for the sort field?

## Data Migration from Level 1 to Level 2

### Database Migration Requirements

- **DM-L2-001**: Add `priority` column as nullable string
- **DM-L2-002**: Add `tags` column as JSONB array with default `[]`
- **DM-L2-003**: Create index on `priority` for sorting
- **DM-L2-004**: Create GIN index on `tags` for array containment queries
- **DM-L2-005**: All existing Level 1 tasks MUST have `priority = null` and `tags = []` after migration
- **DM-L2-006**: Migration MUST be reversible (down migration drops columns)
- **DM-L2-007**: Migration MUST NOT break Level 1 functionality

## Backward Compatibility

- **BC-L2-001**: Level 1 clients MUST continue to work without modification
- **BC-L2-002**: API MUST accept task creation without priority/tags (defaults applied)
- **BC-L2-003**: API responses MUST include priority and tags fields (null/empty for old tasks)
- **BC-L2-004**: Frontend MUST gracefully handle tasks without priority/tags

## Acceptance Gates

Level 2 is considered complete when:

1. All Level 1 functionality still works without regression
2. All Level 2 user stories have passing acceptance tests
3. Database migration is tested and reversible
4. API endpoints for search/filter/sort are fully functional
5. Frontend UI provides all Level 2 features
6. Performance benchmarks (SC-L2-001 through SC-L2-007) are met
7. Edge cases are handled gracefully with clear error messages

## Dependencies

**Depends On**:
- Level 1 (Core) must be complete and validated

**Required Before Level 3**:
- All Level 2 features must be complete
- Database schema must support future date fields (nullable)
- No breaking changes to Level 1 or Level 2 APIs

## Contracts Reference

Detailed contracts are defined in separate files:
- `contracts/sp.api-contract.md` - REST API extensions for Level 2
- `contracts/sp.data-model.md` - Database schema extensions
- `contracts/sp.frontend-behavior.md` - UI behavior for Level 2 features
- `contracts/sp.state-and-lifecycle.md` - State management rules
