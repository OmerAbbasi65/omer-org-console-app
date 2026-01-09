# Phase 2 Execution Plan: Level 2 (Organization) Implementation

**Project**: AI-Native Todo Full-Stack Web Application
**Phase**: Phase 2 - Level 2 (Organization Features)
**Created**: 2026-01-09
**Status**: Planning

---

## Constitutional Alignment

This plan is subordinate to `/sp.constitution` and follows:

1. **Spec-First Development**: All specs complete before implementation begins
2. **Progressive Feature Maturity**: Level 1 → Level 2 → Level 3 (no skipping)
3. **Full-Stack Contract-First**: Frontend and backend designed together
4. **Reusable Intelligence**: Agent skills and subagents as first-class artifacts
5. **No Silent Assumptions**: All decisions explicit and documented

---

## Planning Strategy

### Execution Model

- **Spec-driven**: Specifications define all behavior (already complete)
- **Agent-orchestrated**: Claude agents execute parallelizable work
- **Research-concurrent**: Research happens during implementation, not upfront
- **Contract-first**: API contracts drive frontend/backend integration
- **Progressive rollout**: Level 2 builds on validated Level 1

### Phase Structure

Level 2 implementation follows four phases:

1. **Research** - Validate patterns and technical approach
2. **Foundation** - Database migration and backend API
3. **Analysis** - Frontend components and integration
4. **Synthesis** - Testing, validation, and acceptance

**No phase may be skipped.**

---

## Phase 1: Research

### Objectives

- Establish conceptual correctness without locking implementation details
- Validate database migration strategy (additive-only, backward compatible)
- Validate query optimization patterns (GIN indexes, JSONB queries)
- Validate tag deduplication and normalization algorithms
- Inform implementation with validated patterns

### Research Questions

#### RQ-1: Database Migration Safety

**Question**: How to add `priority` and `tags` fields to existing `tasks` table without breaking Level 1 functionality?

**Research Tasks**:
- Review PostgreSQL ALTER TABLE with live data
- Validate JSONB default value handling (`'[]'::jsonb`)
- Test CHECK constraint on enum field (`priority`)
- Verify Level 1 queries work after migration
- Test rollback strategy (downgrade migration)

**Deliverable**: Migration script validated in test database

**Acceptance**: Level 1 API calls work unchanged after migration

---

#### RQ-2: JSONB Array Query Performance

**Question**: Will GIN index on `tags` field provide acceptable performance for array containment queries?

**Research Tasks**:
- Benchmark `tags @> ARRAY['work']::text[]` on 1,000 tasks
- Compare GIN index vs. no index
- Test multi-tag AND logic: `tags @> ARRAY['work', 'urgent']::text[]`
- Validate EXPLAIN ANALYZE shows index usage
- Measure p95 latency for filter operations

**Deliverable**: Performance benchmark report

**Acceptance**: Filter by tags completes in < 300ms for 1,000 tasks

---

#### RQ-3: Tag Deduplication Strategy

**Question**: Where should tag deduplication happen (frontend, backend, or database)?

**Research Tasks**:
- Evaluate Pydantic validator for deduplication (backend)
- Consider database trigger for deduplication
- Test case-sensitive deduplication ("Work" ≠ "work")
- Validate trimming whitespace from tags

**Deliverable**: Deduplication algorithm specification

**Acceptance**: Duplicate tags never reach database

---

#### RQ-4: Search Algorithm

**Question**: LIKE vs. full-text search for title/description search?

**Research Tasks**:
- Benchmark `LOWER(title) LIKE LOWER('%keyword%')` on 1,000 tasks
- Consider PostgreSQL `tsvector` for full-text search (future)
- Test case-insensitive partial matching
- Validate special character handling (SQL escaping)

**Deliverable**: Search implementation approach

**Acceptance**: Search completes in < 500ms for 1,000 tasks

---

#### RQ-5: Sort Priority Order

**Question**: How to sort by priority enum (high → medium → low → null)?

**Research Tasks**:
- Test CASE statement for priority sorting
- Validate tie-breaking with `created_at`
- Confirm ascending vs. descending order semantics

**Deliverable**: SQL ORDER BY clause for priority

**Acceptance**: Priority sort produces correct order in < 100ms

---

### Research Phase Output

**Deliverables**:
1. Database migration script (tested, reversible)
2. Performance benchmark report (queries, indexes)
3. Tag deduplication algorithm (Pydantic validator)
4. Search query pattern (LIKE-based)
5. Priority sort SQL pattern (CASE statement)

**Validation Gate**:
- All research questions answered
- All benchmarks meet performance targets
- Migration tested with rollback

**Duration Estimate**: 1-2 days (research and validation)

---

## Phase 2: Foundation (Backend)

### Objectives

- Apply database migration (add `priority` and `tags` fields)
- Implement backend API extensions for Level 2
- Validate backward compatibility with Level 1
- Ensure all contracts from `sp.api-contract.md` are implemented

### Foundation Tasks

#### F-1: Database Migration

**Task**: Create and apply Alembic migration for Level 2 fields

**Steps**:
1. Write migration script (upgrade and downgrade)
2. Add `priority` VARCHAR(10) nullable with CHECK constraint
3. Add `tags` JSONB NOT NULL default `'[]'::jsonb`
4. Create index `idx_tasks_priority`
5. Create GIN index `idx_tasks_tags`
6. Test migration on development database
7. Verify Level 1 data integrity (no data loss)
8. Test rollback (downgrade)

**Files Changed**:
- `backend/alembic/versions/002_add_organization_fields.py` (new)

**Validation**:
- Migration applies without errors
- All existing tasks have `priority = NULL` and `tags = []`
- Level 1 API endpoints return correct data (with new fields)
- Rollback restores Level 1 schema

**Dependencies**: Research Phase (RQ-1)

---

#### F-2: SQLModel Schema Extensions

**Task**: Update Task model with Level 2 fields

**Steps**:
1. Add `priority` field to Task model (Optional[str])
2. Add `tags` field to Task model (List[str] with JSON column)
3. Add Pydantic validators (priority enum, tags constraints)
4. Update TaskCreate schema with Level 2 fields
5. Update TaskUpdate schema with Level 2 fields
6. Update TaskResponse schema with Level 2 fields

**Files Changed**:
- `backend/app/models/task.py`

**Validation**:
- All validators enforce constraints (priority enum, max 20 tags, max 50 chars)
- Tag deduplication works correctly
- Whitespace trimming works
- Schema examples in docstrings updated

**Dependencies**: F-1 (migration applied)

---

#### F-3: API Endpoint Extensions

**Task**: Extend existing endpoints to support Level 2 fields

**Steps**:
1. **POST /api/v1/tasks**: Accept `priority` and `tags` in request body
2. **PATCH /api/v1/tasks/{id}**: Accept `priority` and `tags` in request body
3. **GET /api/v1/tasks/{id}**: Return `priority` and `tags` in response
4. Validate all error responses (422 for validation errors)
5. Test backward compatibility (Level 1 requests still work)

**Files Changed**:
- `backend/app/api/v1/tasks.py`

**Validation**:
- Can create task with priority and tags
- Can update priority and tags
- Can set priority to null (remove)
- Can set tags to empty array (remove all)
- Level 1 requests (without Level 2 fields) work unchanged

**Dependencies**: F-2 (schema updated)

---

#### F-4: Query Parameter Support (Filter, Search, Sort)

**Task**: Implement query parameters for GET /api/v1/tasks

**Steps**:
1. Add query parameters: `status`, `priority`, `tag` (multiple), `search`, `sortBy`, `order`
2. Implement filter logic (AND composition)
3. Implement search logic (LIKE-based, case-insensitive)
4. Implement sort logic (priority CASE statement, other fields)
5. Handle invalid query parameter values (400 errors)
6. Return filtered metadata in response (`filters`, `sort`)

**Files Changed**:
- `backend/app/api/v1/tasks.py`

**Validation**:
- Filter by status works
- Filter by priority works (including `priority=none` for null)
- Filter by single tag works
- Filter by multiple tags (AND logic) works
- Search by keyword works (title and description)
- Sort by priority works (high → medium → low → null)
- Sort by title works (case-insensitive alphabetical)
- Sort by createdAt and updatedAt work
- Composite queries (filter + search + sort) work
- Invalid query params return 400 with clear error

**Dependencies**: F-3 (endpoints extended), Research Phase (RQ-2, RQ-4, RQ-5)

---

#### F-5: Backend Testing

**Task**: Write tests for Level 2 backend functionality

**Steps**:
1. Unit tests for Pydantic validators (priority, tags)
2. Unit tests for filter query builder
3. Unit tests for search query builder
4. Unit tests for sort query builder
5. Integration tests for all API endpoints (CRUD + filter/search/sort)
6. Backward compatibility tests (Level 1 requests)

**Files Changed**:
- `backend/tests/unit/test_models.py` (extended)
- `backend/tests/unit/test_validators.py` (new)
- `backend/tests/integration/test_api_level2.py` (new)

**Validation**:
- All tests pass
- Code coverage > 80%
- No regressions in Level 1 tests

**Dependencies**: F-4 (API complete)

---

### Foundation Phase Output

**Deliverables**:
1. Database migration applied (reversible)
2. SQLModel schemas extended
3. API endpoints support Level 2 fields
4. Query parameters for filter/search/sort
5. Backend tests passing (> 80% coverage)

**Validation Gate**:
- All API contracts from `sp.api-contract.md` implemented
- All acceptance criteria from `sp.requirements.md` validated (backend)
- Level 1 functionality unchanged (backward compatibility)
- Performance targets met (< 300ms for filters, < 500ms for search)

**Duration Estimate**: 3-5 days

---

## Phase 3: Analysis (Frontend)

### Objectives

- Implement frontend components for Level 2 features
- Integrate with Level 2 backend API
- Validate UI behavior from `sp.frontend-behavior.md`
- Ensure responsive design and accessibility

### Analysis Tasks

#### A-1: TaskForm Component Extensions

**Task**: Add priority selector and tag input to TaskForm

**Steps**:
1. Add priority dropdown (No Priority, High, Medium, Low)
2. Add tag input field (comma-separated or chip input)
3. Display tag chips below input
4. Implement tag removal (click X on chip)
5. Validate max 20 tags, max 50 chars per tag
6. Update form submission to include priority and tags

**Files Changed**:
- `frontend/app/components/TaskForm.tsx`
- `frontend/app/types.ts` (extend TaskCreate)

**Validation**:
- Can select priority
- Can add tags (comma-separated parsing works)
- Can remove tags (click X)
- Validation errors display correctly
- Form clears after successful submission

**Dependencies**: Foundation Phase (F-4, backend API ready)

---

#### A-2: TaskItem Component Extensions

**Task**: Display priority badge and tags in TaskItem

**Steps**:
1. Add priority badge (color-coded: high=red, medium=yellow, low=green)
2. Display tags as inline chips below description
3. Extend edit mode to include priority selector and tag input
4. Update task update logic to include priority and tags

**Files Changed**:
- `frontend/app/components/TaskItem.tsx`
- `frontend/app/types.ts` (extend TaskUpdate)

**Validation**:
- Priority badge displays with correct color
- Tags display as chips
- Edit mode allows changing priority and tags
- Updates persist to backend

**Dependencies**: A-1 (TaskForm patterns reusable)

---

#### A-3: SearchBar Component

**Task**: Create search input with debounce

**Steps**:
1. Create SearchBar component
2. Implement debounce hook (500ms delay)
3. Add clear button (X icon)
4. Trigger search on debounced value change

**Files Changed**:
- `frontend/app/components/SearchBar.tsx` (new)
- `frontend/app/hooks/useDebounce.ts` (new)

**Validation**:
- Typing updates local state immediately (no lag)
- API call triggered 500ms after typing stops
- Clear button resets search
- Loading state displayed during search

**Dependencies**: Foundation Phase (F-4, search endpoint ready)

---

#### A-4: FilterPanel Component

**Task**: Create filter controls for status, priority, tags

**Steps**:
1. Create FilterPanel component
2. Add status filter (dropdown: All, Incomplete, Completed)
3. Add priority filter (dropdown: All, High, Medium, Low, None)
4. Add tag filter (input with chips, AND logic)
5. Add sort selector (dropdown with all sort options)
6. Add "Clear Filters" button
7. Trigger refetch on filter/sort change

**Files Changed**:
- `frontend/app/components/FilterPanel.tsx` (new)
- `frontend/app/types.ts` (add FilterState, SortState)

**Validation**:
- All filters apply correctly
- Multiple filters use AND logic (composite)
- Sort updates task order
- Clear button resets all filters
- Filter state displayed in UI

**Dependencies**: Foundation Phase (F-4, filter/sort endpoints ready)

---

#### A-5: Main Page State Management

**Task**: Integrate search, filter, sort into main page

**Steps**:
1. Add filter state to page component
2. Add sort state to page component
3. Add search state to page component
4. Build query string from state (URLSearchParams)
5. Call getTasks() with query string
6. Re-fetch on filter/sort/search change (useEffect)
7. Handle loading and error states

**Files Changed**:
- `frontend/app/page.tsx`

**Validation**:
- Changing filters refetches tasks
- Changing sort refetches tasks
- Searching refetches tasks
- Loading skeleton shows during fetch
- Empty state messages display when no results

**Dependencies**: A-3, A-4 (components ready)

---

#### A-6: Server Actions Extensions

**Task**: Update server actions to support query parameters

**Steps**:
1. Extend getTasks() to accept query parameters
2. Keep other actions unchanged (backward compatible)

**Files Changed**:
- `frontend/app/actions/tasks.ts`

**Validation**:
- getTasks() accepts query string
- All Level 1 actions still work

**Dependencies**: Foundation Phase (F-4)

---

#### A-7: Frontend Testing

**Task**: Test Level 2 frontend components

**Steps**:
1. Component tests for TaskForm (with priority/tags)
2. Component tests for TaskItem (display priority/tags)
3. Component tests for SearchBar (debounce)
4. Component tests for FilterPanel
5. Integration tests for main page (full user flow)

**Files Changed**:
- `frontend/app/components/__tests__/` (new tests)

**Validation**:
- All component tests pass
- User flows validated (create → filter → search → sort)

**Dependencies**: A-1 through A-6

---

### Analysis Phase Output

**Deliverables**:
1. TaskForm with priority and tag inputs
2. TaskItem displays priority and tags
3. SearchBar with debounce
4. FilterPanel with all filter/sort controls
5. Main page integrates all Level 2 UI
6. Frontend tests passing

**Validation Gate**:
- All UI behaviors from `sp.frontend-behavior.md` implemented
- All acceptance scenarios from `sp.requirements.md` validated (frontend)
- Responsive design works (mobile, tablet, desktop)
- No regressions in Level 1 UI

**Duration Estimate**: 4-6 days

---

## Phase 4: Synthesis (Integration & Validation)

### Objectives

- End-to-end testing of Level 2 features
- Performance validation
- Acceptance criteria verification
- Documentation updates

### Synthesis Tasks

#### S-1: End-to-End Testing

**Task**: Manual and automated E2E tests for all user stories

**Steps**:
1. Test User Story 1: Task Priorities (all acceptance criteria)
2. Test User Story 2: Task Tags (all acceptance criteria)
3. Test User Story 3: Search Tasks (all acceptance criteria)
4. Test User Story 4: Filter Tasks (all acceptance criteria)
5. Test User Story 5: Sort Tasks (all acceptance criteria)
6. Test all edge cases from `sp.requirements.md`
7. Test backward compatibility (Level 1 flows)

**Validation**:
- All 5 user stories validated
- All acceptance scenarios pass
- All edge cases handled gracefully
- Level 1 functionality unchanged

**Dependencies**: Analysis Phase complete

---

#### S-2: Performance Validation

**Task**: Benchmark and validate performance targets

**Steps**:
1. Benchmark API response times (p50, p95, p99)
2. Benchmark database queries (EXPLAIN ANALYZE)
3. Benchmark frontend rendering (50, 500, 1000 tasks)
4. Load test with 50 concurrent users (optional)
5. Compare against targets in `sp.non-functional.md`

**Validation**:
- All performance targets met or documented exceptions
- No critical bottlenecks identified

**Dependencies**: S-1 (E2E tests passing)

---

#### S-3: Documentation Updates

**Task**: Update README and documentation for Level 2

**Steps**:
1. Update backend README with Level 2 endpoints
2. Update frontend README with Level 2 components
3. Update main README with Level 2 features
4. Create Level 2 testing guide (like Level 1 TESTING.md)
5. Update API documentation (Swagger)

**Files Changed**:
- `backend/README.md`
- `frontend/README.md`
- `PHASE2_README.md`
- `TESTING_LEVEL2.md` (new)

**Validation**:
- All documentation accurate and complete
- Code examples tested and work

**Dependencies**: S-1 (features complete)

---

#### S-4: Acceptance Gate

**Task**: Final validation against acceptance criteria

**Steps**:
1. Review all functional requirements (FR-L2-001 through FR-L2-043)
2. Review all success criteria (SC-L2-001 through SC-L2-007)
3. Verify backward compatibility (BC-L2-001 through BC-L2-004)
4. Verify data migration (DM-L2-001 through DM-L2-007)
5. Sign off on completion

**Validation**:
- All requirements met
- All success criteria achieved
- No critical bugs or regressions

**Dependencies**: S-1, S-2, S-3

---

### Synthesis Phase Output

**Deliverables**:
1. E2E test results (all passing)
2. Performance benchmark report
3. Updated documentation
4. Acceptance sign-off

**Validation Gate**:
- All acceptance criteria from `sp.requirements.md` validated
- All performance targets from `sp.non-functional.md` met
- All documentation updated
- Level 2 ready for production

**Duration Estimate**: 2-3 days

---

## Parallel Execution Strategy

### Parallelizable Work

**Research Phase**:
- RQ-1, RQ-2, RQ-3, RQ-4, RQ-5 can be researched in parallel (5 concurrent agents)

**Foundation Phase**:
- F-1 must complete first (migration)
- F-2, F-3 can run after F-1 (2 concurrent agents)
- F-4 depends on F-2, F-3
- F-5 runs after F-4

**Analysis Phase**:
- A-1, A-3, A-4 can run in parallel (3 concurrent agents)
- A-2 depends on A-1 (reuse patterns)
- A-5, A-6 depend on A-1, A-3, A-4
- A-7 runs after all components complete

**Synthesis Phase**:
- S-1, S-2, S-3 can run in parallel
- S-4 depends on S-1, S-2, S-3

### Critical Path

```
Research (all RQs) → F-1 → F-2/F-3 → F-4 → F-5 → A-1 → A-2 → A-5 → A-6 → A-7 → S-1 → S-4
                                                    ↓
                                                A-3, A-4 → A-5
```

**Estimated Total Duration**: 10-16 days (with parallelization)

---

## Quality Enforcement Rules

1. **No implementation without passing validation gate**
   - Each phase must complete validation before next phase starts

2. **No feature without acceptance criteria**
   - All acceptance scenarios from user stories must be testable

3. **No agent without a spec**
   - Reusable intelligence must be specified before implementation

4. **No undocumented decisions**
   - All architectural decisions must be recorded (ADR if significant)

5. **No breaking changes**
   - Level 1 functionality must remain unchanged (backward compatibility)

---

## Definition of Done: Level 2

Level 2 is complete when:

1. ✅ All 5 user stories validated (37 acceptance scenarios passing)
2. ✅ All 43 functional requirements implemented (FR-L2-001 through FR-L2-043)
3. ✅ All 7 success criteria achieved (SC-L2-001 through SC-L2-007)
4. ✅ Database migration applied and tested (reversible)
5. ✅ Backend API contracts fully implemented (`sp.api-contract.md`)
6. ✅ Frontend UI behaviors fully implemented (`sp.frontend-behavior.md`)
7. ✅ All performance targets met (`sp.non-functional.md`)
8. ✅ Level 1 functionality unchanged (backward compatibility verified)
9. ✅ Code coverage > 80% (backend and frontend)
10. ✅ Documentation updated (README, TESTING, API docs)
11. ✅ No critical bugs or regressions

---

## Risk Mitigation

### Risk 1: Database Migration Failure

**Impact**: Level 1 data corrupted or lost
**Likelihood**: Low
**Mitigation**:
- Test migration on copy of production data
- Have rollback script ready
- Backup database before migration
- Test Level 1 queries after migration

### Risk 2: Performance Degradation

**Impact**: Queries too slow with filters/search
**Likelihood**: Medium
**Mitigation**:
- Benchmark early (Research Phase)
- Add indexes proactively
- Use EXPLAIN ANALYZE to validate
- Consider pagination if needed (defer to Level 3)

### Risk 3: Backward Compatibility Break

**Impact**: Level 1 clients stop working
**Likelihood**: Low
**Mitigation**:
- Maintain Level 1 test suite
- Run Level 1 tests after each change
- Validate API responses include new fields (but Level 1 ignores them)

### Risk 4: Tag Deduplication Bugs

**Impact**: Duplicate tags in database
**Likelihood**: Medium
**Mitigation**:
- Comprehensive unit tests for deduplication
- Test with edge cases (case sensitivity, whitespace)
- Validate at both frontend and backend

---

## Next Actions

1. **Immediate**: Begin Research Phase (RQ-1 through RQ-5)
2. **Upon research completion**: Begin Foundation Phase (F-1 migration)
3. **Upon foundation completion**: Begin Analysis Phase (A-1 components)
4. **Upon analysis completion**: Begin Synthesis Phase (S-1 E2E testing)

**Estimated Completion**: 10-16 days from start

---

## Constitutional Compliance

✅ **Spec-First**: All specs complete before this plan
✅ **Progressive Maturity**: Builds on Level 1, prepares for Level 3
✅ **Full-Stack Contract-First**: API contracts drive frontend/backend
✅ **Reusable Intelligence**: Subagents and skills specified
✅ **No Silent Assumptions**: All decisions explicit in this plan
✅ **Traceability**: Spec → Architecture → Implementation → Validation
