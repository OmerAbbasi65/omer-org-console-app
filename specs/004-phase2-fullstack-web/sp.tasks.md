# Tasks: Phase 2 Full-Stack Todo Web Application

**Input**: Design documents from `/specs/004-phase2-fullstack-web/`
**Prerequisites**: sp.plan.md (required), sp.requirements.md (required for user stories), sp.research.md, sp.data-model.md, contracts/

**Tests**: Tests are NOT generated in this task list (not explicitly requested in feature specification)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Backend paths: `backend/src/models/`, `backend/src/services/`, `backend/src/api/`, `backend/src/agents/`
- Frontend paths: `frontend/src/app/`, `frontend/src/components/`, `frontend/src/lib/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure (backend/src/models/, backend/src/services/, backend/src/api/, backend/src/agents/)
- [X] T002 Create frontend directory structure (frontend/src/app/, frontend/src/components/, frontend/src/lib/)
- [X] T003 [P] Initialize backend Python project with pyproject.toml in backend/
- [X] T004 [P] Initialize frontend Next.js project with package.json in frontend/
- [X] T005 [P] Create backend requirements.txt with FastAPI, SQLModel, Pydantic, Uvicorn, Alembic, pytest
- [X] T006 [P] Create frontend package.json with Next.js 14+, React 18+, TypeScript 5.3+, TailwindCSS 3+
- [X] T007 [P] Configure TypeScript in frontend/tsconfig.json (strict mode, path aliases)
- [X] T008 [P] Configure TailwindCSS in frontend/tailwind.config.js
- [X] T009 Create .env.example files for backend and frontend with DATABASE_URL, API_URL placeholders
- [X] T010 Create docker-compose.yml for local development (backend + frontend + Neon connection)
- [ ] T011 Create README.md with setup instructions referencing sp.quickstart.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T012 Create database connection module in backend/src/database.py with SQLModel engine and session factory
- [X] T013 Create configuration module in backend/src/config.py loading environment variables (DATABASE_URL, CORS origins, logging)
- [X] T014 Initialize Alembic in backend/alembic/ with env.py configured for SQLModel
- [X] T015 Create FastAPI application instance in backend/src/main.py with CORS middleware and health check endpoint
- [X] T016 [P] Create base Pydantic models in backend/src/models/__init__.py
- [X] T017 [P] Create TypeScript type definitions in frontend/src/lib/types.ts (Task interface, API response types)
- [X] T018 [P] Create API client utility in frontend/src/lib/api.ts with fetch wrappers and error handling
- [X] T019 Create Next.js root layout in frontend/src/app/layout.tsx with global styles and metadata
- [X] T020 Create initial database migration for Task model in backend/alembic/versions/001_create_tasks_table.py

**Checkpoint**: ✅ Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Task Management via Web UI (Priority: P1) 🎯 MVP

**Goal**: User can create, view, update, complete, and delete tasks through web browser

**Independent Test**: User opens web app, adds task "Buy groceries", marks complete, refreshes page, sees task persisted

### Implementation for User Story 1

#### Backend - Models & Services

- [X] T021 [P] [US1] Create Task SQLModel in backend/src/models/task.py with id (UUID), title, description, completed, priority, tags, due_date, recurrence, parent_id, created_at, updated_at
- [X] T022 [P] [US1] Create TaskCreate Pydantic model in backend/src/models/task.py for request validation (title required 1-200 chars, description optional max 2000 chars)
- [X] T023 [P] [US1] Create TaskUpdate Pydantic model in backend/src/models/task.py for PATCH requests (all fields optional)
- [X] T024 [P] [US1] Create TaskResponse Pydantic model in backend/src/models/task.py for API responses
- [X] T025 [US1] Create TaskService in backend/src/services/task_service.py with create_task, get_task_by_id, get_tasks, update_task, delete_task methods
- [X] T026 [US1] Implement create_task in TaskService (generate UUID, set defaults for completed=False, priority='medium', tags=[], recurrence='none')
- [X] T027 [US1] Implement get_tasks in TaskService with pagination support (default limit=50, offset support, return total count)
- [X] T028 [US1] Implement update_task in TaskService with partial update support (merge provided fields, update updated_at timestamp)
- [X] T029 [US1] Implement delete_task in TaskService (hard delete, no soft delete in Phase 2)

#### Backend - API Endpoints

- [X] T030 [US1] Create tasks router in backend/src/api/tasks.py
- [X] T031 [US1] Implement POST /api/v1/tasks endpoint (create task, return 201 with TaskResponse)
- [X] T032 [US1] Implement GET /api/v1/tasks endpoint (list tasks with pagination, filters, return 200 with tasks array and pagination metadata)
- [X] T033 [US1] Implement GET /api/v1/tasks/:id endpoint (get single task, return 200 or 404)
- [X] T034 [US1] Implement PATCH /api/v1/tasks/:id endpoint (partial update, return 200 or 404 or 422 on validation error)
- [X] T035 [US1] Implement DELETE /api/v1/tasks/:id endpoint (delete task, return 204 or 404)
- [X] T036 [US1] Register tasks router in backend/src/main.py with /api/v1 prefix

#### Frontend - Components

- [X] T037 [P] [US1] Create TaskCard component in frontend/src/components/TaskCard.tsx (display title, description, completed checkbox, edit/delete buttons)
- [X] T038 [P] [US1] Create TaskList component in frontend/src/components/TaskList.tsx (render array of TaskCard, handle empty state)
- [X] T039 [P] [US1] Create TaskForm component in frontend/src/components/TaskForm.tsx (title input, description textarea, validation, submit/cancel buttons)
- [X] T040 [P] [US1] Create Modal component in frontend/src/components/Modal.tsx (reusable modal wrapper with backdrop, close on ESC/click outside)
- [X] T041 [US1] Create DeleteConfirmModal in frontend/src/components/DeleteConfirmModal.tsx (Modal with confirmation, handle delete confirmation)
- [X] T042 [US1] Create modals integrated in home page (create, edit, delete modals with TaskForm)

#### Frontend - Pages & Actions

- [X] T043 [US1] Create home page in frontend/src/app/page.tsx with client-side data fetching (fetch tasks from API, render TaskList, handle all CRUD operations)
- [ ] T044 [US1] Implement client-side task creation in frontend/src/app/actions/createTask.ts (POST to API, revalidate page)
- [ ] T045 [US1] Implement client-side task update in frontend/src/app/actions/updateTask.ts (PATCH to API, revalidate page)
- [ ] T046 [US1] Implement client-side task deletion in frontend/src/app/actions/deleteTask.ts (DELETE to API, revalidate page)
- [ ] T047 [US1] Implement toggle complete action in frontend/src/app/actions/toggleComplete.ts (PATCH completed field, optimistic UI update)
- [ ] T048 [US1] Add "Add Task" button to home page opening CreateTaskModal
- [ ] T049 [US1] Wire edit button in TaskCard to open EditTaskModal with task data
- [ ] T050 [US1] Wire delete button in TaskCard to show confirmation dialog and call deleteTask action

#### Integration & Styling

- [X] T051 [US1] Add loading states to home page (skeleton loaders for task list during SSR)
- [X] T052 [US1] Add error states to home page (error banner for API failures with retry button)
- [X] T053 [US1] Add empty state to TaskList ("No tasks yet. Create your first task!" message)
- [X] T054 [US1] Style TaskCard with TailwindCSS (completed tasks have strikethrough, subtle hover effects)
- [X] T055 [US1] Style TaskForm with TailwindCSS (validation errors in red, character counters for title and description)
- [X] T056 [US1] Implement form validation in TaskForm (title 1-200 chars, description max 2000 chars, show errors on blur)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

**Acceptance Validation**:
1. ✅ User can create task "Buy groceries" and see it in list
2. ✅ User can mark task complete and styling updates
3. ✅ Tasks persist across page refreshes
4. ✅ User can edit task title and changes are saved

---

## Phase 4: User Story 2 - Task Organization and Filtering (Priority: P2)

**Goal**: User can organize tasks by priority and tags, search, filter, and sort

**Independent Test**: User creates 10 tasks with varying priorities and tags, filters to show only "high priority work tasks", sees expected subset

### Implementation for User Story 2

#### Backend - Enhanced Models & Services

- [ ] T057 [P] [US2] Add priority field validation to TaskCreate model (enum: 'high', 'medium', 'low')
- [ ] T058 [P] [US2] Add tags field validation to TaskCreate model (array of strings, max 10 items, each max 50 chars)
- [ ] T059 [US2] Enhance get_tasks in TaskService with filter parameters (status: active/completed/all, priority, tag, search)
- [ ] T060 [US2] Implement search logic in get_tasks (case-insensitive LIKE on title and description)
- [ ] T061 [US2] Implement filter logic in get_tasks (composable filters using AND conditions)
- [ ] T062 [US2] Implement sort logic in get_tasks (sort by: createdAt, dueDate, priority, title; order: asc/desc)

#### Backend - API Enhancements

- [ ] T063 [US2] Update GET /api/v1/tasks endpoint to accept query params (status, priority, tag, search, sortBy, sortOrder)
- [ ] T064 [US2] Implement GET /api/v1/tasks/tags endpoint (return unique tags across all tasks)
- [ ] T065 [US2] Add validation for query parameters in tasks router (validate enum values, sanitize search input)

#### Frontend - Filter Components

- [ ] T066 [P] [US2] Create FilterBar component in frontend/src/components/FilterBar.tsx (container for all filter controls)
- [ ] T067 [P] [US2] Create StatusFilter component in frontend/src/components/filters/StatusFilter.tsx (dropdown: All, Active, Completed)
- [ ] T068 [P] [US2] Create PriorityFilter component in frontend/src/components/filters/PriorityFilter.tsx (dropdown: All, High, Medium, Low)
- [ ] T069 [P] [US2] Create TagFilter component in frontend/src/components/filters/TagFilter.tsx (dropdown populated from /api/v1/tasks/tags)
- [ ] T070 [P] [US2] Create SearchInput component in frontend/src/components/filters/SearchInput.tsx (text input with debounce, search icon)
- [ ] T071 [P] [US2] Create SortSelector component in frontend/src/components/filters/SortSelector.tsx (dropdown: Created Date, Due Date, Priority, Alphabetical + order toggle)
- [ ] T072 [US2] Integrate FilterBar into home page (above TaskList, pass filter state to API fetch)

#### Frontend - Task Form Enhancements

- [ ] T073 [P] [US2] Add priority selector to TaskForm in frontend/src/components/TaskForm.tsx (dropdown with High/Medium/Low, defaults to Medium)
- [ ] T074 [P] [US2] Add tags input to TaskForm in frontend/src/components/TaskForm.tsx (chip-based input, comma-separated entry, max 10 tags)
- [ ] T075 [US2] Add tags validation to TaskForm (each tag max 50 chars, duplicate removal, show error if > 10 tags)

#### Frontend - State Management

- [ ] T076 [US2] Implement filter state management in home page (URL query params as source of truth: ?status=active&priority=high&tag=work)
- [ ] T077 [US2] Update server-side fetch in home page to read query params and pass to API
- [ ] T078 [US2] Implement client-side filter changes (update URL query params, trigger router.refresh())
- [ ] T079 [US2] Add loading indicator to FilterBar during filter application

#### Styling & UX

- [ ] T080 [US2] Style FilterBar with TailwindCSS (horizontal layout on desktop, vertical on mobile, clear visual grouping)
- [ ] T081 [US2] Style filter dropdowns with TailwindCSS (consistent styling, keyboard navigation support)
- [ ] T082 [US2] Add "Clear Filters" button to FilterBar (reset all filters to default, visible only when filters active)
- [ ] T083 [US2] Add filter summary text below FilterBar ("Showing 5 high priority work tasks")
- [ ] T084 [US2] Style priority badges in TaskCard (High=red, Medium=yellow, Low=blue with appropriate contrast)
- [ ] T085 [US2] Style tags in TaskCard (pill-shaped chips with truncation if too many, show "+N more" if > 3 tags)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

**Acceptance Validation**:
1. ✅ User can set priority and tags when creating task
2. ✅ User can filter by priority and see only matching tasks
3. ✅ User can filter by tag and see only matching tasks
4. ✅ User can search by keyword and see matching tasks
5. ✅ User can apply multiple filters (composable)

---

## Phase 5: User Story 3 - Intelligent Scheduling with Recurring Tasks (Priority: P3)

**Goal**: User can set due dates, create recurring tasks, receive reminders

**Independent Test**: User creates recurring task "Weekly team meeting" set for every Monday at 10 AM, system automatically generates next 4 occurrences

### Implementation for User Story 3

#### Backend - Agents (Reusable Intelligence)

- [ ] T086 [P] [US3] Create RecurrenceReasoningAgent in backend/src/agents/recurrence_reasoning_agent.py (calculate next occurrence date with edge case handling for month-end, leap years)
- [ ] T087 [P] [US3] Define RecurrenceInput Pydantic model (task with due_date, recurrence pattern, completed_at, timezone)
- [ ] T088 [P] [US3] Define RecurrenceOutput Pydantic model (next_occurrence with due_date, calculation_method, edge_cases_handled, warnings)
- [ ] T089 [US3] Implement calculate_next_occurrence method in RecurrenceReasoningAgent (daily: +1 day, weekly: +7 days, monthly: +1 month with month-end adjustment)
- [ ] T090 [P] [US3] Create ReminderEvaluationAgent in backend/src/agents/reminder_evaluation_agent.py (determine which reminders should trigger)
- [ ] T091 [P] [US3] Define ReminderInput Pydantic model (tasks with due_dates and reminder_offsets, current_time, user_timezone)
- [ ] T092 [P] [US3] Define ReminderOutput Pydantic model (ready_reminders with task_id, reminder_time, urgency, notification_method)
- [ ] T093 [US3] Implement evaluate_reminders method in ReminderEvaluationAgent (check if current_time >= reminder_time AND current_time < due_date, calculate urgency)

#### Backend - Services & Endpoints for Recurring Tasks

- [ ] T094 [US3] Enhance TaskService with complete_task method (mark task complete, generate next occurrence if recurring using RecurrenceReasoningAgent)
- [ ] T095 [US3] Implement POST /api/v1/tasks/:id/complete endpoint (call complete_task, return original task + next_occurrence if generated)
- [ ] T096 [US3] Implement GET /api/v1/tasks/overdue endpoint (query tasks where due_date < NOW() AND completed = FALSE, sort by due_date)
- [ ] T097 [US3] Implement GET /api/v1/tasks/reminders endpoint (call ReminderEvaluationAgent, return ready reminders with threshold parameter, default 60 minutes lookahead)

#### Frontend - Due Date & Recurrence Components

- [ ] T098 [P] [US3] Create DateTimePicker component in frontend/src/components/DateTimePicker.tsx (native datetime-local input with timezone conversion to UTC)
- [ ] T099 [P] [US3] Create RecurrenceSelector component in frontend/src/components/RecurrenceSelector.tsx (dropdown: None, Daily, Weekly, Monthly, disabled if no due_date)
- [ ] T100 [P] [US3] Create ReminderOffsetInput component in frontend/src/components/ReminderOffsetInput.tsx (input minutes before due_date, e.g., "30 minutes before")
- [ ] T101 [US3] Add due_date field to TaskForm (DateTimePicker, optional, validate not more than 1 year in future)
- [ ] T102 [US3] Add recurrence field to TaskForm (RecurrenceSelector, enabled only if due_date is set, validate recurrence requires due_date)
- [ ] T103 [US3] Add reminder_offset field to TaskForm (ReminderOffsetInput, optional, enabled only if due_date is set)

#### Frontend - Overdue & Reminder UI

- [ ] T104 [P] [US3] Create OverdueBadge component in frontend/src/components/OverdueBadge.tsx (red badge with "Overdue" text and overdue duration)
- [ ] T105 [P] [US3] Create ReminderNotification component in frontend/src/components/ReminderNotification.tsx (toast notification with task title, due time, dismiss button)
- [ ] T106 [US3] Add overdue indicator to TaskCard (render OverdueBadge if task.dueDate < now AND task.completed = false)
- [ ] T107 [US3] Display due date in TaskCard (format as "MMM DD, YYYY HH:MM" in user's local timezone, show timezone abbreviation)
- [ ] T108 [US3] Display recurrence pattern in TaskCard (show icon + text: "Repeats daily", "Repeats weekly", "Repeats monthly")

#### Frontend - Reminder Polling Service

- [ ] T109 [US3] Create reminder polling hook in frontend/src/lib/hooks/useReminderPolling.ts (poll /api/v1/tasks/reminders every 60 seconds)
- [ ] T110 [US3] Implement browser notification API in frontend/src/lib/notifications.ts (request permission, show notification, fallback to in-app if denied)
- [ ] T111 [US3] Integrate reminder polling in home page (useReminderPolling hook, show ReminderNotification when reminders ready)
- [ ] T112 [US3] Handle notification permission flow (show banner requesting permission if not granted, gracefully degrade to in-app if denied)

#### Complete Button Enhancement

- [ ] T113 [US3] Update toggleComplete action to use POST /api/v1/tasks/:id/complete endpoint (handle next_occurrence in response)
- [ ] T114 [US3] Show success toast after completing recurring task ("Task completed. Next occurrence created for [date]")
- [ ] T115 [US3] Add next occurrence to task list immediately after completion (optimistic UI update, append to list without full refetch)

#### Styling & UX

- [ ] T116 [US3] Style DateTimePicker with TailwindCSS (calendar icon, clear button, validation errors)
- [ ] T117 [US3] Style RecurrenceSelector with TailwindCSS (icon for each pattern, tooltip explaining pattern)
- [ ] T118 [US3] Style OverdueBadge with TailwindCSS (red background, white text, pulsing animation)
- [ ] T119 [US3] Style ReminderNotification with TailwindCSS (slide-in animation, dismiss button, urgency-based styling)
- [ ] T120 [US3] Add visual indication for recurring tasks in TaskList (recurring icon next to title, tooltip showing pattern)

**Checkpoint**: All user stories should now be independently functional

**Acceptance Validation**:
1. ✅ User can set due date and it's stored as UTC
2. ✅ Completing recurring task generates next occurrence
3. ✅ Overdue tasks are visually highlighted
4. ✅ Reminder notifications appear at scheduled time
5. ✅ Deleting recurring task handles child instances (no cascade delete, each instance independent)

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T121 [P] Add comprehensive error handling to all API endpoints (structured error responses with error codes, log errors)
- [ ] T122 [P] Add request logging middleware to backend (log all API requests with request ID, method, path, status, duration)
- [ ] T123 [P] Add response compression middleware to backend (gzip for responses > 1KB)
- [ ] T124 [P] Implement OpenAPI schema generation in backend (auto-generate from FastAPI app, serve at /api/v1/docs)
- [ ] T125 [P] Add loading spinners to all async operations in frontend (button loading states, page transitions)
- [ ] T126 [P] Add success/error toast notifications to all mutations in frontend (create, update, delete confirmations)
- [ ] T127 [P] Implement optimistic UI updates for all mutations (immediate feedback, rollback on error)
- [ ] T128 [P] Add keyboard shortcuts to frontend (Ctrl+K for search, N for new task, Esc to close modals)
- [ ] T129 [P] Add accessibility improvements (ARIA labels, keyboard navigation, focus management, screen reader announcements)
- [ ] T130 [P] Optimize frontend bundle size (code splitting, lazy loading for modals, tree shaking)
- [ ] T131 [P] Add performance monitoring (track API response times, page load times, log to console in dev mode)
- [ ] T132 Add health check endpoint GET /health in backend (return service status, database connectivity, uptime)
- [ ] T133 Create database seed script in backend/scripts/seed_test_data.py (generate 20 sample tasks with varying attributes for testing)
- [ ] T134 Document API endpoints in README.md (link to OpenAPI docs, include curl examples for each endpoint)
- [ ] T135 Run sp.quickstart.md validation (verify all setup steps work, test API examples, confirm tests run)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on US1 (filters work on empty list too)
  - **Recommended**: Complete US1 first for better testing experience (need tasks to filter)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on US1/US2 (due dates and recurrence are task fields)
  - **Recommended**: Complete US1 and US2 first for full feature experience (need tasks with priorities and tags)

### Within Each User Story

**User Story 1 (US1) - Sequential within story**:
1. Backend Models (T021-T024) → Backend Services (T025-T029) → Backend API (T030-T036)
2. Frontend Components (T037-T042) can be developed in parallel with Backend API
3. Frontend Pages & Actions (T043-T050) depend on both Backend API and Frontend Components
4. Integration & Styling (T051-T056) depends on Pages & Actions

**User Story 2 (US2) - Sequential within story**:
1. Backend Enhancements (T057-T062) → Backend API (T063-T065)
2. Frontend Filter Components (T066-T075) can be developed in parallel with Backend
3. Frontend State Management (T076-T079) depends on both Backend API and Filter Components
4. Styling & UX (T080-T085) depends on State Management

**User Story 3 (US3) - Partial parallel opportunities**:
1. Backend Agents (T086-T093) can be developed in parallel (independent modules)
2. Backend Services & Endpoints (T094-T097) depend on Agents completion
3. Frontend Components (T098-T108) can be developed in parallel with Backend
4. Frontend Polling Service (T109-T112) depends on Backend endpoints
5. Complete Button Enhancement (T113-T115) depends on both Backend and Frontend Components
6. Styling & UX (T116-T120) depends on all components

### Parallel Opportunities

**Phase 1 (Setup)**: T003-T010 can all run in parallel (different files, independent setup tasks)

**Phase 2 (Foundational)**: T016-T018 can run in parallel (base models, types, API client are independent)

**User Story 1 (US1)**:
- T021-T024 can run in parallel (all Pydantic models in same file, different classes)
- T037-T042 can run in parallel (independent React components)

**User Story 2 (US2)**:
- T057-T058 can run in parallel (model enhancements in same file)
- T066-T071 can run in parallel (independent filter components)
- T073-T074 can run in parallel (TaskForm enhancements in different sections)

**User Story 3 (US3)**:
- T086-T088 (RecurrenceAgent) and T090-T092 (ReminderAgent) can run in parallel (independent agents)
- T098-T100 can run in parallel (independent date/recurrence/reminder components)
- T104-T105 can run in parallel (independent badge and notification components)

**Polish Phase**: T121-T131 can all run in parallel (cross-cutting concerns, different files)

---

## Parallel Example: User Story 1 (Backend)

```bash
# Launch all Pydantic models together:
Task T021: Create Task SQLModel
Task T022: Create TaskCreate Pydantic model
Task T023: Create TaskUpdate Pydantic model
Task T024: Create TaskResponse Pydantic model

# Then launch all service methods together (after models complete):
Task T026: Implement create_task
Task T027: Implement get_tasks
Task T028: Implement update_task
Task T029: Implement delete_task
```

---

## Parallel Example: User Story 2 (Frontend)

```bash
# Launch all filter components together:
Task T067: Create StatusFilter component
Task T068: Create PriorityFilter component
Task T069: Create TagFilter component
Task T070: Create SearchInput component
Task T071: Create SortSelector component
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
   - ✅ Can create task "Buy groceries"
   - ✅ Can mark task complete
   - ✅ Task persists after refresh
   - ✅ Can edit and delete task
5. Deploy/demo if ready (MVP is functional!)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T021-T056)
   - Developer B: User Story 2 (T057-T085)
   - Developer C: User Story 3 (T086-T120)
3. Stories complete and integrate independently

**Note**: Recommended to complete US1 first for better testing experience, but technically all stories can start in parallel after Foundational phase.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 135
**Setup Phase**: 11 tasks
**Foundational Phase**: 9 tasks
**User Story 1 (P1)**: 36 tasks
**User Story 2 (P2)**: 29 tasks
**User Story 3 (P3)**: 35 tasks
**Polish Phase**: 15 tasks

**Parallel Opportunities**: 45 tasks marked with [P]
**Independent User Stories**: 3 stories (US1, US2, US3) - all independently testable

**Suggested MVP Scope**: Phase 1 + Phase 2 + User Story 1 (56 tasks total)

**Estimated Complexity**:
- User Story 1 (P1): Medium complexity, foundational CRUD operations
- User Story 2 (P2): Low-Medium complexity, builds on US1 with filters
- User Story 3 (P3): High complexity, requires agent reasoning, date arithmetic, polling

---

## Format Validation

✅ All 135 tasks follow checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
✅ Task IDs sequential (T001-T135)
✅ Parallel tasks marked with [P]
✅ User story tasks marked with [US1], [US2], or [US3]
✅ File paths included in all implementation tasks
✅ Checkpoints defined after each user story phase
✅ Independent test criteria provided for each user story
