# Executable Tasks: Level 2 (Organization) Implementation

**Project**: AI-Native Todo Full-Stack Web Application
**Phase**: Phase 2 - Level 2 (Organization Features)
**Created**: 2026-01-09
**Status**: Ready for Execution

---

## Task Execution Rules

1. **Sequential Execution**: Tasks must be executed in order within each phase
2. **Validation Required**: Each task must pass validation before proceeding
3. **Parallel Execution**: Tasks marked `[PARALLEL]` can run concurrently
4. **Blocking Tasks**: Tasks marked `[BLOCKING]` must complete before dependent tasks start
5. **Test Cases**: All tasks include specific test cases for validation

---

## Phase 1: Research (1-2 days)

### Task R-1: Validate Database Migration Strategy [PARALLEL]

**Objective**: Ensure additive-only migration works without breaking Level 1

**Steps**:
1. Create test database with Level 1 schema
2. Insert 100 test tasks (Level 1 format)
3. Write migration script (upgrade + downgrade)
4. Apply migration on test database
5. Verify all Level 1 tasks have `priority = NULL` and `tags = []`
6. Run Level 1 API queries (SELECT, WHERE completed = false)
7. Test rollback (downgrade migration)
8. Verify Level 1 schema restored

**Test Cases**:
```sql
-- TC-R1-1: After migration, all tasks have default values
SELECT COUNT(*) FROM tasks WHERE priority IS NULL AND tags = '[]'::jsonb;
-- Expected: 100 (all tasks)

-- TC-R1-2: Level 1 query still works
SELECT id, title, description, completed FROM tasks WHERE completed = false;
-- Expected: Returns all incomplete tasks without errors

-- TC-R1-3: After rollback, Level 2 columns removed
SELECT column_name FROM information_schema.columns WHERE table_name = 'tasks';
-- Expected: Only Level 1 columns present (no priority, no tags)
```

**Acceptance Criteria**:
- ✅ Migration applies without errors
- ✅ All existing tasks have default Level 2 values
- ✅ Level 1 queries return correct data
- ✅ Rollback restores Level 1 schema exactly

**Deliverable**: `alembic/versions/002_add_organization_fields.py` (draft)

**Duration**: 2-4 hours

---

### Task R-2: Benchmark JSONB Array Query Performance [PARALLEL]

**Objective**: Validate GIN index provides acceptable performance for tag filtering

**Steps**:
1. Create test database with 1,000 tasks
2. Assign random tags to tasks (1-5 tags each)
3. Create GIN index: `CREATE INDEX idx_tasks_tags ON tasks USING GIN(tags);`
4. Benchmark query: `SELECT * FROM tasks WHERE tags @> ARRAY['work']::text[]`
5. Measure execution time (EXPLAIN ANALYZE)
6. Benchmark multi-tag query: `WHERE tags @> ARRAY['work', 'urgent']::text[]`
7. Compare performance with and without GIN index

**Test Cases**:
```sql
-- TC-R2-1: Single tag filter (with index)
EXPLAIN ANALYZE SELECT * FROM tasks WHERE tags @> ARRAY['work']::text[];
-- Expected: Execution time < 100ms, uses GIN index

-- TC-R2-2: Multi-tag filter (with index)
EXPLAIN ANALYZE SELECT * FROM tasks WHERE tags @> ARRAY['work', 'urgent']::text[];
-- Expected: Execution time < 150ms, uses GIN index

-- TC-R2-3: Without index (baseline)
DROP INDEX idx_tasks_tags;
EXPLAIN ANALYZE SELECT * FROM tasks WHERE tags @> ARRAY['work']::text[];
-- Expected: Execution time > 500ms, sequential scan
```

**Acceptance Criteria**:
- ✅ Single tag filter < 100ms with GIN index
- ✅ Multi-tag filter < 150ms with GIN index
- ✅ GIN index shown in EXPLAIN ANALYZE output

**Deliverable**: Performance benchmark report (markdown)

**Duration**: 1-2 hours

---

### Task R-3: Design Tag Deduplication Algorithm [PARALLEL]

**Objective**: Define where and how tag deduplication happens

**Steps**:
1. Write Pydantic validator for tags field
2. Test deduplication: `["work", "work", "urgent"]` → `["work", "urgent"]`
3. Test case sensitivity: `["Work", "work"]` → keeps both
4. Test whitespace trimming: `[" work ", "urgent"]` → `["work", "urgent"]`
5. Test empty tag rejection: `["", "work"]` → `["work"]`
6. Test order preservation: `["urgent", "work", "urgent"]` → `["urgent", "work"]`

**Test Cases**:
```python
# TC-R3-1: Duplicate removal (case-sensitive)
tags = ["work", "work", "urgent"]
result = deduplicate_tags(tags)
assert result == ["work", "urgent"]

# TC-R3-2: Case sensitivity preserved
tags = ["Work", "work"]
result = deduplicate_tags(tags)
assert result == ["Work", "work"]  # Different cases kept

# TC-R3-3: Whitespace trimming
tags = [" work ", "  urgent  "]
result = deduplicate_tags(tags)
assert result == ["work", "urgent"]

# TC-R3-4: Empty tag rejection
tags = ["", "work", "   ", "urgent"]
result = deduplicate_tags(tags)
assert result == ["work", "urgent"]

# TC-R3-5: Order preserved (first occurrence kept)
tags = ["urgent", "work", "urgent", "deploy"]
result = deduplicate_tags(tags)
assert result == ["urgent", "work", "deploy"]
```

**Acceptance Criteria**:
- ✅ Duplicates removed (case-sensitive)
- ✅ Whitespace trimmed
- ✅ Empty tags rejected
- ✅ Order preserved

**Deliverable**: Pydantic validator function (code + tests)

**Duration**: 1-2 hours

---

### Task R-4: Validate Search Query Performance [PARALLEL]

**Objective**: Ensure LIKE-based search meets performance targets

**Steps**:
1. Create test database with 1,000 tasks
2. Add varied titles and descriptions
3. Benchmark query: `WHERE LOWER(title) LIKE LOWER('%keyword%')`
4. Benchmark with description: `WHERE LOWER(title) LIKE '%k%' OR LOWER(description) LIKE '%k%'`
5. Test special character escaping (%, _, \)
6. Measure p50, p95, p99 latencies

**Test Cases**:
```sql
-- TC-R4-1: Title search (case-insensitive)
EXPLAIN ANALYZE
SELECT * FROM tasks
WHERE LOWER(title) LIKE LOWER('%groceries%');
-- Expected: < 200ms

-- TC-R4-2: Title + description search
EXPLAIN ANALYZE
SELECT * FROM tasks
WHERE LOWER(title) LIKE '%groceries%'
   OR LOWER(description) LIKE '%groceries%';
-- Expected: < 500ms

-- TC-R4-3: Special character escaping
SELECT * FROM tasks WHERE LOWER(title) LIKE '%\%%';
-- Expected: No SQL errors, matches tasks with '%' in title
```

**Acceptance Criteria**:
- ✅ Search completes in < 500ms for 1,000 tasks
- ✅ Case-insensitive matching works
- ✅ Special characters handled safely

**Deliverable**: Search query pattern (SQL + validation)

**Duration**: 1-2 hours

---

### Task R-5: Design Priority Sort Algorithm [PARALLEL]

**Objective**: Define SQL ORDER BY for priority enum sorting

**Steps**:
1. Write CASE statement for priority order
2. Test ascending: high → medium → low → null
3. Test descending: null → low → medium → high
4. Test tie-breaking with created_at
5. Validate performance (< 100ms for 1,000 tasks)

**Test Cases**:
```sql
-- TC-R5-1: Priority sort ascending (high first)
SELECT title, priority FROM tasks
ORDER BY
  CASE priority
    WHEN 'high' THEN 1
    WHEN 'medium' THEN 2
    WHEN 'low' THEN 3
    ELSE 4
  END ASC,
  created_at DESC
LIMIT 10;
-- Expected: High priority tasks first, then medium, low, null

-- TC-R5-2: Priority sort descending (null first)
SELECT title, priority FROM tasks
ORDER BY
  CASE priority
    WHEN 'high' THEN 1
    WHEN 'medium' THEN 2
    WHEN 'low' THEN 3
    ELSE 4
  END DESC,
  created_at DESC
LIMIT 10;
-- Expected: Null priority tasks first, then low, medium, high

-- TC-R5-3: Performance check
EXPLAIN ANALYZE SELECT * FROM tasks ORDER BY priority;
-- Expected: < 100ms for 1,000 tasks
```

**Acceptance Criteria**:
- ✅ Priority sort produces correct order
- ✅ Tie-breaking with created_at works
- ✅ Performance < 100ms

**Deliverable**: SQL ORDER BY pattern (with CASE)

**Duration**: 1 hour

---

**Research Phase Validation Gate**:
- All 5 research tasks complete
- All test cases passing
- All acceptance criteria met
- Performance benchmarks documented

---

## Phase 2: Foundation (Backend) (3-5 days)

### Task F-1: Apply Database Migration [BLOCKING]

**Objective**: Add priority and tags fields to tasks table

**Steps**:
1. Copy migration draft from R-1 to `alembic/versions/`
2. Review migration script (upgrade + downgrade)
3. Apply migration: `alembic upgrade head`
4. Verify schema: `\d tasks` (in psql)
5. Verify indexes: `\di` (check idx_tasks_priority, idx_tasks_tags)
6. Check constraint: Priority enum validation
7. Test Level 1 data integrity

**Test Cases**:
```bash
# TC-F1-1: Migration applies successfully
alembic upgrade head
# Expected: "Running upgrade 001 -> 002, add_organization_fields"

# TC-F1-2: Schema includes new columns
psql -c "\d tasks"
# Expected: priority VARCHAR(10), tags JSONB

# TC-F1-3: Indexes created
psql -c "\di"
# Expected: idx_tasks_priority, idx_tasks_tags (GIN)

# TC-F1-4: Check constraint enforced
psql -c "INSERT INTO tasks (title, priority) VALUES ('Test', 'critical');"
# Expected: ERROR - violates check constraint

# TC-F1-5: Existing tasks have defaults
psql -c "SELECT COUNT(*) FROM tasks WHERE priority IS NULL AND tags = '[]'::jsonb;"
# Expected: All existing tasks
```

**Acceptance Criteria**:
- ✅ Migration applies without errors
- ✅ Schema includes priority and tags
- ✅ Indexes created (B-tree on priority, GIN on tags)
- ✅ Check constraint enforces priority enum
- ✅ All existing tasks have default values

**Deliverable**: Migration applied to database

**Duration**: 1 hour

**Dependencies**: R-1 complete

---

### Task F-2: Update SQLModel Schemas [BLOCKING]

**Objective**: Extend Task model with Level 2 fields

**Steps**:
1. Add `priority` field to Task model
2. Add `tags` field to Task model (JSON column)
3. Add Pydantic validator for priority (enum check)
4. Add Pydantic validator for tags (from R-3)
5. Update TaskCreate schema
6. Update TaskUpdate schema
7. Update TaskResponse schema
8. Update schema examples in docstrings

**Test Cases**:
```python
# TC-F2-1: Create task with priority and tags
task = TaskCreate(
    title="Deploy app",
    priority="high",
    tags=["work", "urgent"]
)
assert task.priority == "high"
assert task.tags == ["work", "urgent"]

# TC-F2-2: Invalid priority rejected
with pytest.raises(ValidationError):
    TaskCreate(title="Test", priority="critical")

# TC-F2-3: Tags deduplicated
task = TaskCreate(
    title="Test",
    tags=["work", "work", "urgent"]
)
assert task.tags == ["work", "urgent"]

# TC-F2-4: Too many tags rejected
with pytest.raises(ValidationError):
    TaskCreate(title="Test", tags=["tag" + str(i) for i in range(21)])

# TC-F2-5: Tag too long rejected
with pytest.raises(ValidationError):
    TaskCreate(title="Test", tags=["a" * 51])

# TC-F2-6: Whitespace trimmed
task = TaskCreate(title="Test", tags=[" work ", "urgent"])
assert task.tags == ["work", "urgent"]
```

**Acceptance Criteria**:
- ✅ Task model includes priority and tags
- ✅ Validators enforce all constraints
- ✅ Deduplication works correctly
- ✅ All test cases pass

**Deliverable**: `backend/app/models/task.py` (updated)

**Duration**: 2-3 hours

**Dependencies**: F-1 complete, R-3 complete

---

### Task F-3: Extend API Endpoints (CRUD)

**Objective**: Accept and return Level 2 fields in CRUD endpoints

**Steps**:
1. Update POST /tasks to accept priority and tags
2. Update PATCH /tasks/{id} to accept priority and tags
3. Update GET /tasks/{id} to return priority and tags
4. Update GET /tasks to return priority and tags
5. Test backward compatibility (Level 1 requests)
6. Test validation errors (422 responses)

**Test Cases**:
```python
# TC-F3-1: Create task with priority and tags
response = client.post("/api/v1/tasks", json={
    "title": "Deploy app",
    "priority": "high",
    "tags": ["work", "urgent"]
})
assert response.status_code == 201
assert response.json()["data"]["priority"] == "high"
assert response.json()["data"]["tags"] == ["work", "urgent"]

# TC-F3-2: Create task without Level 2 fields (backward compat)
response = client.post("/api/v1/tasks", json={
    "title": "Simple task"
})
assert response.status_code == 201
assert response.json()["data"]["priority"] is None
assert response.json()["data"]["tags"] == []

# TC-F3-3: Update priority
response = client.patch("/api/v1/tasks/{id}", json={
    "priority": "medium"
})
assert response.status_code == 200
assert response.json()["data"]["priority"] == "medium"

# TC-F3-4: Update tags (replace all)
response = client.patch("/api/v1/tasks/{id}", json={
    "tags": ["work", "deployment"]
})
assert response.status_code == 200
assert response.json()["data"]["tags"] == ["work", "deployment"]

# TC-F3-5: Remove priority (set to null)
response = client.patch("/api/v1/tasks/{id}", json={
    "priority": None
})
assert response.status_code == 200
assert response.json()["data"]["priority"] is None

# TC-F3-6: Invalid priority rejected
response = client.post("/api/v1/tasks", json={
    "title": "Test",
    "priority": "critical"
})
assert response.status_code == 422
assert "priority" in response.json()["error"]["message"].lower()
```

**Acceptance Criteria**:
- ✅ CRUD endpoints accept Level 2 fields
- ✅ CRUD endpoints return Level 2 fields
- ✅ Level 1 requests still work (backward compat)
- ✅ Validation errors return 422 with clear messages

**Deliverable**: `backend/app/api/v1/tasks.py` (updated)

**Duration**: 2-3 hours

**Dependencies**: F-2 complete

---

### Task F-4: Implement Query Parameters (Filter)

**Objective**: Add filtering by status, priority, tags

**Steps**:
1. Add query parameter parsing to GET /tasks
2. Implement status filter (`?status=incomplete`)
3. Implement priority filter (`?priority=high`)
4. Implement tag filter (`?tag=work&tag=urgent` - AND logic)
5. Implement composite filters (all criteria must match)
6. Return filter metadata in response
7. Validate invalid parameters (400 errors)

**Test Cases**:
```python
# TC-F4-1: Filter by status
response = client.get("/api/v1/tasks?status=incomplete")
assert response.status_code == 200
assert all(not task["completed"] for task in response.json()["data"]["tasks"])

# TC-F4-2: Filter by priority
response = client.get("/api/v1/tasks?priority=high")
assert response.status_code == 200
assert all(task["priority"] == "high" for task in response.json()["data"]["tasks"])

# TC-F4-3: Filter by priority "none" (null)
response = client.get("/api/v1/tasks?priority=none")
assert response.status_code == 200
assert all(task["priority"] is None for task in response.json()["data"]["tasks"])

# TC-F4-4: Filter by single tag
response = client.get("/api/v1/tasks?tag=work")
assert response.status_code == 200
assert all("work" in task["tags"] for task in response.json()["data"]["tasks"])

# TC-F4-5: Filter by multiple tags (AND logic)
response = client.get("/api/v1/tasks?tag=work&tag=urgent")
assert response.status_code == 200
for task in response.json()["data"]["tasks"]:
    assert "work" in task["tags"] and "urgent" in task["tags"]

# TC-F4-6: Composite filter (status + priority + tags)
response = client.get("/api/v1/tasks?status=incomplete&priority=high&tag=work")
assert response.status_code == 200
for task in response.json()["data"]["tasks"]:
    assert not task["completed"]
    assert task["priority"] == "high"
    assert "work" in task["tags"]

# TC-F4-7: Invalid status value
response = client.get("/api/v1/tasks?status=pending")
assert response.status_code == 400
assert "invalid" in response.json()["error"]["message"].lower()

# TC-F4-8: Invalid priority value
response = client.get("/api/v1/tasks?priority=critical")
assert response.status_code == 400
```

**Acceptance Criteria**:
- ✅ All filter types work independently
- ✅ Composite filters use AND logic
- ✅ Filter metadata returned in response
- ✅ Invalid parameters return 400 with clear errors

**Deliverable**: `backend/app/api/v1/tasks.py` (filter logic added)

**Duration**: 3-4 hours

**Dependencies**: F-3 complete, R-2 complete

---

### Task F-5: Implement Query Parameters (Search)

**Objective**: Add keyword search in title and description

**Steps**:
1. Add search query parameter (`?search=keyword`)
2. Implement case-insensitive LIKE search
3. Search both title and description (OR logic)
4. Handle special characters (SQL escaping)
5. Return search metadata in response

**Test Cases**:
```python
# TC-F5-1: Search in title
response = client.get("/api/v1/tasks?search=groceries")
assert response.status_code == 200
for task in response.json()["data"]["tasks"]:
    assert "groceries" in task["title"].lower() or "groceries" in (task["description"] or "").lower()

# TC-F5-2: Case-insensitive search
response = client.get("/api/v1/tasks?search=URGENT")
assert response.status_code == 200
# Should match "urgent", "Urgent", "URGENT"

# TC-F5-3: Partial match
response = client.get("/api/v1/tasks?search=gro")
assert response.status_code == 200
# Should match "groceries", "grow", etc.

# TC-F5-4: Search in description
response = client.get("/api/v1/tasks?search=milk")
assert response.status_code == 200
# Should match tasks with "milk" in description

# TC-F5-5: No results
response = client.get("/api/v1/tasks?search=nonexistent123")
assert response.status_code == 200
assert response.json()["data"]["tasks"] == []
assert response.json()["data"]["total"] == 0

# TC-F5-6: Special characters (% _ \)
response = client.get("/api/v1/tasks?search=100%")
assert response.status_code == 200
# Should not cause SQL error
```

**Acceptance Criteria**:
- ✅ Search works in title and description
- ✅ Case-insensitive matching
- ✅ Partial matches work
- ✅ Special characters handled safely
- ✅ Performance < 500ms for 1,000 tasks

**Deliverable**: `backend/app/api/v1/tasks.py` (search logic added)

**Duration**: 2-3 hours

**Dependencies**: F-4 complete, R-4 complete

---

### Task F-6: Implement Query Parameters (Sort)

**Objective**: Add sorting by priority, title, dates

**Steps**:
1. Add sortBy and order query parameters
2. Implement priority sort (CASE statement from R-5)
3. Implement title sort (case-insensitive alphabetical)
4. Implement createdAt and updatedAt sort
5. Validate sort fields (400 for invalid)
6. Return sort metadata in response

**Test Cases**:
```python
# TC-F6-1: Sort by priority (high to low)
response = client.get("/api/v1/tasks?sortBy=priority&order=desc")
assert response.status_code == 200
# Verify order: high, medium, low, null

# TC-F6-2: Sort by title (A-Z)
response = client.get("/api/v1/tasks?sortBy=title&order=asc")
assert response.status_code == 200
titles = [task["title"] for task in response.json()["data"]["tasks"]]
assert titles == sorted(titles, key=str.lower)

# TC-F6-3: Sort by createdAt (newest first)
response = client.get("/api/v1/tasks?sortBy=createdAt&order=desc")
assert response.status_code == 200
# Verify newest tasks first

# TC-F6-4: Default sort (createdAt desc)
response = client.get("/api/v1/tasks")
assert response.status_code == 200
assert response.json()["data"]["sort"]["by"] == "createdAt"
assert response.json()["data"]["sort"]["order"] == "desc"

# TC-F6-5: Invalid sortBy field
response = client.get("/api/v1/tasks?sortBy=dueDate")
assert response.status_code == 400

# TC-F6-6: Invalid order value
response = client.get("/api/v1/tasks?sortBy=title&order=random")
assert response.status_code == 400
```

**Acceptance Criteria**:
- ✅ All sort fields work correctly
- ✅ Ascending and descending both work
- ✅ Default sort applied when not specified
- ✅ Invalid parameters return 400
- ✅ Performance < 100ms for 1,000 tasks

**Deliverable**: `backend/app/api/v1/tasks.py` (sort logic added)

**Duration**: 2-3 hours

**Dependencies**: F-5 complete, R-5 complete

---

### Task F-7: Backend Unit Tests

**Objective**: Test all Level 2 backend logic

**Steps**:
1. Test Pydantic validators (priority, tags)
2. Test filter query builder
3. Test search query builder
4. Test sort query builder
5. Run all tests: `pytest backend/tests/`

**Test Cases**: See individual test files

**Acceptance Criteria**:
- ✅ All tests pass
- ✅ Code coverage > 80%
- ✅ No regressions in Level 1 tests

**Deliverable**: Test files in `backend/tests/`

**Duration**: 4-6 hours

**Dependencies**: F-6 complete

---

**Foundation Phase Validation Gate**:
- All backend tasks complete (F-1 through F-7)
- All test cases passing
- API contracts from `sp.api-contract.md` implemented
- Performance targets met
- Backward compatibility verified

---

## Phase 3: Analysis (Frontend) (4-6 days)

### Task A-1: Extend TaskForm Component

**Objective**: Add priority selector and tag input

**Steps**:
1. Add priority dropdown to TaskForm
2. Add tag input field (comma-separated)
3. Display tag chips below input
4. Add tag removal (X button on chips)
5. Validate max 20 tags, max 50 chars
6. Update form submission logic

**Test Cases**:
```typescript
// TC-A1-1: Select priority
// User selects "High" from dropdown
// Expected: priority state updates to "high"

// TC-A1-2: Add tags (comma-separated)
// User types "work, urgent" and presses Enter
// Expected: Tags ["work", "urgent"] display as chips

// TC-A1-3: Remove tag
// User clicks X on "urgent" chip
// Expected: Tag removed, only "work" remains

// TC-A1-4: Max tags validation
// User tries to add 21st tag
// Expected: Error "Maximum 20 tags allowed"

// TC-A1-5: Tag too long
// User types tag with 51 characters
// Expected: Error "Tag exceeds 50 character limit"

// TC-A1-6: Form submission with Level 2 fields
// User submits with priority="high", tags=["work"]
// Expected: API called with correct payload, task created
```

**Acceptance Criteria**:
- ✅ Priority selector works
- ✅ Tag input parses comma-separated values
- ✅ Tag chips display and are removable
- ✅ Validation errors display correctly
- ✅ Form submits with Level 2 fields

**Deliverable**: `frontend/app/components/TaskForm.tsx` (updated)

**Duration**: 3-4 hours

**Dependencies**: Foundation Phase complete

---

### Task A-2: Extend TaskItem Component

**Objective**: Display priority badge and tags

**Steps**:
1. Add priority badge (color-coded)
2. Display tags as inline chips
3. Extend edit mode with priority and tag controls
4. Update task update logic

**Test Cases**:
```typescript
// TC-A2-1: Display priority badge
// Task has priority="high"
// Expected: Red "HIGH" badge displays

// TC-A2-2: Display tags
// Task has tags=["work", "urgent"]
// Expected: Two gray chips display below description

// TC-A2-3: Edit priority
// User clicks Edit, changes priority from "high" to "medium"
// Expected: Priority updates on save

// TC-A2-4: Edit tags
// User clicks Edit, adds tag "deployment"
// Expected: Tags update to ["work", "urgent", "deployment"]

// TC-A2-5: Priority colors
// High=red, Medium=yellow, Low=green
// Expected: Correct colors display
```

**Acceptance Criteria**:
- ✅ Priority badge displays with correct color
- ✅ Tags display as chips
- ✅ Edit mode includes Level 2 controls
- ✅ Updates persist to backend

**Deliverable**: `frontend/app/components/TaskItem.tsx` (updated)

**Duration**: 3-4 hours

**Dependencies**: A-1 complete (reuse patterns)

---

### Task A-3: Create SearchBar Component [PARALLEL with A-4]

**Objective**: Search input with 500ms debounce

**Steps**:
1. Create SearchBar component
2. Implement useDebounce hook
3. Add clear button (X icon)
4. Trigger search on debounced value

**Test Cases**:
```typescript
// TC-A3-1: Typing updates local state
// User types "groceries"
// Expected: Input shows "groceries" immediately

// TC-A3-2: Debounce triggers search
// User stops typing for 500ms
// Expected: API called with search term

// TC-A3-3: Clear button
// User clicks X icon
// Expected: Search cleared, all tasks shown

// TC-A3-4: Rapid typing
// User types quickly (< 500ms between keystrokes)
// Expected: Only final term triggers API call
```

**Acceptance Criteria**:
- ✅ Search input responsive (no lag)
- ✅ Debounce works (500ms delay)
- ✅ Clear button resets search
- ✅ Loading state shows during fetch

**Deliverable**: `frontend/app/components/SearchBar.tsx` (new)

**Duration**: 2-3 hours

**Dependencies**: Foundation Phase complete

---

### Task A-4: Create FilterPanel Component [PARALLEL with A-3]

**Objective**: Filter controls for status, priority, tags

**Steps**:
1. Create FilterPanel component
2. Add status filter dropdown
3. Add priority filter dropdown
4. Add tag filter input
5. Add sort selector
6. Add "Clear Filters" button
7. Trigger refetch on filter change

**Test Cases**:
```typescript
// TC-A4-1: Filter by status
// User selects "Incomplete" from dropdown
// Expected: Only incomplete tasks shown

// TC-A4-2: Filter by priority
// User selects "High" from dropdown
// Expected: Only high-priority tasks shown

// TC-A4-3: Filter by tag
// User enters "work" in tag filter
// Expected: Only tasks with "work" tag shown

// TC-A4-4: Multiple tag filters (AND logic)
// User adds "work" and "urgent"
// Expected: Only tasks with BOTH tags shown

// TC-A4-5: Clear filters
// User clicks "Clear Filters"
// Expected: All filters reset, all tasks shown

// TC-A4-6: Sort selector
// User selects "Priority (High to Low)"
// Expected: Tasks reordered by priority
```

**Acceptance Criteria**:
- ✅ All filter types work
- ✅ Composite filters use AND logic
- ✅ Sort changes task order
- ✅ Clear button resets everything

**Deliverable**: `frontend/app/components/FilterPanel.tsx` (new)

**Duration**: 4-5 hours

**Dependencies**: Foundation Phase complete

---

### Task A-5: Integrate Components into Main Page

**Objective**: Wire search, filter, sort into page state

**Steps**:
1. Add filter state to page component
2. Add sort state to page component
3. Add search state to page component
4. Build query string from state
5. Call getTasks() with query params
6. Re-fetch on state changes (useEffect)

**Test Cases**:
```typescript
// TC-A5-1: Filter triggers refetch
// User changes filter
// Expected: API called with new filter params

// TC-A5-2: Search triggers refetch
// User types in search (debounced)
// Expected: API called with search param

// TC-A5-3: Sort triggers refetch
// User changes sort
// Expected: API called with sort params

// TC-A5-4: Multiple filters trigger single fetch
// User changes filter and sort simultaneously
// Expected: Single API call with all params

// TC-A5-5: Loading state
// During fetch
// Expected: Loading skeleton shows

// TC-A5-6: Empty state
// No tasks match filters
// Expected: "No tasks match filters" message
```

**Acceptance Criteria**:
- ✅ State changes trigger refetch
- ✅ Query params built correctly
- ✅ Loading and empty states work
- ✅ No duplicate API calls

**Deliverable**: `frontend/app/page.tsx` (updated)

**Duration**: 3-4 hours

**Dependencies**: A-1, A-2, A-3, A-4 complete

---

### Task A-6: Update Server Actions

**Objective**: Extend getTasks to accept query parameters

**Steps**:
1. Modify getTasks() signature to accept query string
2. Append query string to API URL
3. Keep other actions unchanged

**Test Cases**:
```typescript
// TC-A6-1: getTasks with query params
const tasks = await getTasks("status=incomplete&priority=high");
// Expected: API called with query string

// TC-A6-2: getTasks without params (backward compat)
const tasks = await getTasks();
// Expected: API called without query string

// TC-A6-3: Level 1 actions unchanged
const task = await createTask({title: "Test"});
// Expected: Still works without Level 2 fields
```

**Acceptance Criteria**:
- ✅ getTasks accepts query string
- ✅ Level 1 actions still work
- ✅ Backward compatible

**Deliverable**: `frontend/app/actions/tasks.ts` (updated)

**Duration**: 1 hour

**Dependencies**: Foundation Phase complete

---

### Task A-7: Frontend Component Tests

**Objective**: Test all Level 2 frontend components

**Steps**:
1. Test TaskForm (priority, tags)
2. Test TaskItem (display, edit)
3. Test SearchBar (debounce)
4. Test FilterPanel (all filters)
5. Test page integration

**Test Cases**: See individual component tests

**Acceptance Criteria**:
- ✅ All component tests pass
- ✅ User flows validated

**Deliverable**: Component test files

**Duration**: 4-6 hours

**Dependencies**: A-1 through A-6 complete

---

**Analysis Phase Validation Gate**:
- All frontend tasks complete (A-1 through A-7)
- All test cases passing
- UI behaviors from `sp.frontend-behavior.md` implemented
- Responsive design verified
- No Level 1 regressions

---

## Phase 4: Synthesis (Integration & Validation) (2-3 days)

### Task S-1: End-to-End Testing (User Stories)

**Objective**: Validate all 5 user stories

**Steps**:
1. Test User Story 1: Task Priorities (6 scenarios)
2. Test User Story 2: Task Tags (6 scenarios)
3. Test User Story 3: Search Tasks (6 scenarios)
4. Test User Story 4: Filter Tasks (7 scenarios)
5. Test User Story 5: Sort Tasks (7 scenarios)
6. Test all edge cases from spec
7. Test Level 1 regression (backward compat)

**Test Cases**:
```
User Story 1 - Task Priorities:
- ✅ US1-AC1: Create task with priority "high"
- ✅ US1-AC2: Update priority from "medium" to "high"
- ✅ US1-AC3: Visual distinction of priorities (colors)
- ✅ US1-AC4: Display "No priority" for null
- ✅ US1-AC5: Create task without priority (defaults to null)

User Story 2 - Task Tags:
- ✅ US2-AC1: Create task with multiple tags
- ✅ US2-AC2: Add tag to existing task
- ✅ US2-AC3: Remove individual tag
- ✅ US2-AC4: Task with no tags displays nothing
- ✅ US2-AC5: Duplicate tags deduplicated
- ✅ US2-AC6: Tags display as badges

User Story 3 - Search Tasks:
- ✅ US3-AC1: Search in title (partial match)
- ✅ US3-AC2: Case-insensitive search
- ✅ US3-AC3: Partial keyword matching
- ✅ US3-AC4: No results message
- ✅ US3-AC5: Clear search shows all tasks
- ✅ US3-AC6: Search in description

User Story 4 - Filter Tasks:
- ✅ US4-AC1: Filter by status
- ✅ US4-AC2: Filter by priority
- ✅ US4-AC3: Filter by tag
- ✅ US4-AC4: Composite filters (AND logic)
- ✅ US4-AC5: Multiple tag filters (AND)
- ✅ US4-AC6: No results message
- ✅ US4-AC7: Clear filters

User Story 5 - Sort Tasks:
- ✅ US5-AC1: Sort by priority (high to low)
- ✅ US5-AC2: Sort by title (A-Z)
- ✅ US5-AC3: Sort by created date (newest first)
- ✅ US5-AC4: Sort by created date (oldest first)
- ✅ US5-AC5: Changing sort replaces previous
- ✅ US5-AC6: Sort not persisted on refresh
- ✅ US5-AC7: Null priority tasks last in priority sort
```

**Acceptance Criteria**:
- ✅ All 32 acceptance scenarios pass
- ✅ All edge cases handled gracefully
- ✅ Level 1 functionality unchanged

**Deliverable**: E2E test results document

**Duration**: 6-8 hours

**Dependencies**: Analysis Phase complete

---

### Task S-2: Performance Validation

**Objective**: Verify all performance targets met

**Steps**:
1. Benchmark API response times (filter, search, sort)
2. Benchmark database queries (EXPLAIN ANALYZE)
3. Benchmark frontend rendering (50, 500, 1000 tasks)
4. Compare against targets in `sp.non-functional.md`
5. Document any deviations

**Test Cases**:
```
Performance Targets:
- ✅ GET /tasks (no filters): < 200ms (p95)
- ✅ GET /tasks (with filters): < 300ms (p95)
- ✅ GET /tasks (with search): < 500ms (p95)
- ✅ GET /tasks (composite): < 600ms (p95)
- ✅ Filter by tags: < 150ms (1000 tasks)
- ✅ Search: < 500ms (1000 tasks)
- ✅ Sort by priority: < 100ms (1000 tasks)
- ✅ Frontend render: < 100ms (50 tasks)
- ✅ Frontend render: < 300ms (500 tasks)
```

**Acceptance Criteria**:
- ✅ All performance targets met or exceptions documented
- ✅ No critical bottlenecks

**Deliverable**: Performance benchmark report

**Duration**: 2-3 hours

**Dependencies**: S-1 complete

---

### Task S-3: Documentation Updates

**Objective**: Update all documentation for Level 2

**Steps**:
1. Update backend README (Level 2 endpoints)
2. Update frontend README (Level 2 components)
3. Update main PHASE2_README (Level 2 features)
4. Create TESTING_LEVEL2.md (E2E test checklist)
5. Update API documentation (Swagger)

**Deliverables**:
- `backend/README.md` (updated)
- `frontend/README.md` (updated)
- `PHASE2_README.md` (updated)
- `TESTING_LEVEL2.md` (new)

**Duration**: 2-3 hours

**Dependencies**: S-1, S-2 complete

---

### Task S-4: Final Acceptance Gate

**Objective**: Validate all acceptance criteria

**Steps**:
1. Review all 43 functional requirements (FR-L2-001 to FR-L2-043)
2. Review all 7 success criteria (SC-L2-001 to SC-L2-007)
3. Verify backward compatibility (BC-L2-001 to BC-L2-004)
4. Verify data migration (DM-L2-001 to DM-L2-007)
5. Sign off on Level 2 completion

**Checklist**:
```
Functional Requirements:
- ✅ FR-L2-001 to FR-L2-043: All implemented

Success Criteria:
- ✅ SC-L2-001: Assign priority in < 5 seconds
- ✅ SC-L2-002: Add tags in < 10 seconds
- ✅ SC-L2-003: Search < 2 seconds (1000 tasks)
- ✅ SC-L2-004: Filters < 1 second (1000 tasks)
- ✅ SC-L2-005: Sorting < 500ms (1000 tasks)
- ✅ SC-L2-006: Composite filters 100% correct
- ✅ SC-L2-007: Tag deduplication 100% correct

Backward Compatibility:
- ✅ BC-L2-001: Level 1 clients work unchanged
- ✅ BC-L2-002: API accepts tasks without Level 2 fields
- ✅ BC-L2-003: Responses include Level 2 fields
- ✅ BC-L2-004: Frontend handles tasks without Level 2 data

Data Migration:
- ✅ DM-L2-001: priority column added (nullable)
- ✅ DM-L2-002: tags column added (JSONB, default [])
- ✅ DM-L2-003: priority index created
- ✅ DM-L2-004: tags GIN index created
- ✅ DM-L2-005: Existing tasks have defaults
- ✅ DM-L2-006: Migration reversible
- ✅ DM-L2-007: No Level 1 breakage
```

**Acceptance Criteria**:
- ✅ All requirements met
- ✅ All success criteria achieved
- ✅ No critical bugs

**Deliverable**: Level 2 completion sign-off

**Duration**: 2-3 hours

**Dependencies**: S-1, S-2, S-3 complete

---

**Synthesis Phase Validation Gate**:
- All synthesis tasks complete (S-1 through S-4)
- All acceptance criteria validated
- Level 2 ready for production

---

## Summary

**Total Tasks**: 27 executable tasks across 4 phases

**Estimated Duration**: 10-16 days

**Parallel Execution**:
- Research: 5 tasks in parallel
- Foundation: Sequential with some parallelism
- Analysis: Up to 3 tasks in parallel
- Synthesis: Up to 3 tasks in parallel

**Key Milestones**:
1. Research complete (Day 2)
2. Backend complete (Day 7)
3. Frontend complete (Day 13)
4. Level 2 validated (Day 16)

**Definition of Done**:
- ✅ All 27 tasks complete
- ✅ All test cases passing
- ✅ All acceptance criteria met
- ✅ Documentation updated
- ✅ Level 2 production-ready
