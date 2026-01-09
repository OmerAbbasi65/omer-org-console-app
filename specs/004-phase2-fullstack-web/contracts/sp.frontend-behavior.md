# Frontend Behavior: Phase 2 Todo Web Application

**Feature**: 004-phase2-fullstack-web
**Created**: 2026-01-09
**Framework**: Next.js 14+ (App Router)
**UI Constraints**: No direct database access, no embedded business logic

## Core Principles

1. **Stateless UI by Default**: State lives in backend or controlled stores, not implicit component state
2. **Server-Side Rendering First**: Initial page load uses SSR for performance and SEO
3. **API-Driven**: All data operations via backend API; no direct database access
4. **Progressive Enhancement**: Core functionality works without JavaScript; enhanced with client-side interactivity
5. **Separation of Concerns**: UI components, server actions, and API calls are separate modules

---

## Page-Level Behavior

### Home Page (`/`)

**Purpose**: Primary task management interface

**Data-Fetching Strategy**:
- **Server Component**: Initial render fetches tasks via server-side API call to `/api/v1/tasks`
- **Query Parameters**: URL query params control filters, sorting, pagination (e.g., `/` `?status=active&priority=high&page=2`)
- **Revalidation**: Page revalidates on navigation using Next.js router refresh

**Sections**:
1. **Header**: App title, task count summary, add task button
2. **Filters Bar**: Dropdowns for status, priority, tags; search input; sort selector
3. **Task List**: Paginated table/list of tasks with inline actions (complete, edit, delete)
4. **Footer**: Pagination controls

**Loading States**:
- **Initial Load**: Skeleton loaders for task list (3-5 placeholder rows)
- **Filter Change**: Show loading indicator on filter bar while fetching
- **Pagination**: Disable pagination buttons during fetch, show spinner

**Error States**:
- **Network Error**: Display error banner "Unable to load tasks. Check connection." with retry button
- **Empty State**: If no tasks match filters, show "No tasks found. Try adjusting filters or create a new task."
- **API Error (500)**: Display "Something went wrong. Please try again later."

**Interactions**:
- **Add Task**: Opens modal/drawer with task creation form
- **Complete Toggle**: Click checkbox to mark task complete (optimistic UI update, API call in background)
- **Edit Task**: Click edit icon to open edit modal/drawer with pre-filled form
- **Delete Task**: Click delete icon, show confirmation dialog, delete on confirm
- **Filter/Sort**: Update URL query params, trigger page refetch with new params

---

### Task Detail Page (`/tasks/[id]`)

**Purpose**: View and edit single task in detail

**Data-Fetching Strategy**:
- **Server Component**: Fetches task via `/api/v1/tasks/:id` on server
- **Revalidation**: Revalidates on mount if navigating from another page

**Sections**:
1. **Task Header**: Title, completion status, priority badge
2. **Task Body**: Description (rich text display), tags, due date, recurrence pattern
3. **Actions**: Edit button, delete button, complete/uncomplete toggle
4. **Metadata**: Created date, last updated date

**Loading States**:
- **Initial Load**: Full-page skeleton loader with title, description, metadata placeholders

**Error States**:
- **404**: "Task not found. It may have been deleted."
- **Network Error**: "Unable to load task. Check connection." with back button
- **API Error**: "Something went wrong. Please try again."

**Interactions**:
- **Edit Mode**: Click edit button to switch to inline edit form
- **Save Changes**: Submit form, show loading spinner on save button, display success toast on save
- **Delete**: Confirmation dialog, redirect to home on successful deletion

---

### Task Creation Modal

**Trigger**: Click "Add Task" button on home page

**Form Fields**:
1. **Title** (required): Text input, max 200 chars, live character count
2. **Description** (optional): Textarea, max 2000 chars, live character count
3. **Priority** (optional): Dropdown (High, Medium, Low), defaults to Medium
4. **Tags** (optional): Tag input (comma-separated or chip-based), max 10 tags
5. **Due Date** (optional): Datetime picker (date + time), defaults to no due date
6. **Recurrence** (optional): Dropdown (None, Daily, Weekly, Monthly), enabled only if due date set

**Loading States**:
- **Form Submission**: Disable submit button, show spinner, prevent duplicate submissions

**Error States**:
- **Validation Errors**: Inline error messages below each field (e.g., "Title is required")
- **API Error**: Display error message above form "Failed to create task. Please try again."

**Success State**:
- **Close Modal**: Modal closes automatically on success
- **Toast Notification**: Show success toast "Task created successfully"
- **List Update**: Task list refreshes to include new task

**Interactions**:
- **Cancel**: Close modal without saving, no API call
- **Save**: Validate form, POST to `/api/v1/tasks`, handle response

---

### Task Edit Modal

**Trigger**: Click "Edit" button on task card or detail page

**Form Fields**: Same as Task Creation Modal, pre-filled with current task data

**Loading States**:
- **Initial Load**: Pre-fill form fields with fetched task data (if not already available)
- **Form Submission**: Disable save button, show spinner

**Error States**:
- **Validation Errors**: Inline error messages
- **API Error**: "Failed to update task. Please try again."
- **Concurrent Edit Conflict**: "Task was modified by another session. Refresh and try again." (Phase 2: last write wins, no conflict resolution)

**Success State**:
- **Close Modal**: Modal closes on success
- **Toast Notification**: "Task updated successfully"
- **List Update**: Task list refreshes to reflect changes

**Interactions**:
- **Cancel**: Close modal, discard changes
- **Save**: PATCH to `/api/v1/tasks/:id`, handle response

---

## Data-Fetching Expectations

### Server-Side Fetching (Initial Load)

```
Page Component (Server) → API Call to Backend → Database Query → Render HTML with Data
```

- Use Next.js `fetch` with `cache: 'no-store'` for always-fresh data (or appropriate cache strategy)
- Handle errors gracefully with fallback UI
- Pass data as props to client components

### Client-Side Fetching (Interactions)

```
User Action (Button Click) → Client Component → API Call → Update Local State → Re-render
```

- Use `fetch` or `axios` in client components
- Show loading indicators during fetch
- Optimistic UI updates for better perceived performance (e.g., mark task complete immediately, revert on error)

### Revalidation Strategy

- **On-Demand**: User actions (create, update, delete) trigger refetch via `router.refresh()`
- **No Automatic Polling**: Phase 2 does not implement real-time updates; user must manually refresh for changes from other sessions
- **Reminder Polling**: Frontend polls `/api/v1/tasks/reminders` every 60 seconds for pending reminders (Level 3 feature)

---

## Loading and Error States

### Loading States (UX Patterns)

| Interaction         | Loading Indicator                                    | Duration Expectation   |
|---------------------|------------------------------------------------------|------------------------|
| Initial page load   | Full-page skeleton with task list placeholders       | 1-3 seconds            |
| Filter change       | Loading spinner on filter bar, task list greyed out  | < 1 second             |
| Task creation       | Disabled submit button with spinner                  | < 1 second             |
| Task update         | Disabled save button with spinner                    | < 1 second             |
| Task deletion       | Loading spinner in confirmation dialog               | < 1 second             |
| Pagination          | Disabled pagination buttons, spinner on active page  | < 1 second             |

**Guidelines**:
- Use skeleton loaders for initial content load (better UX than blank screen)
- Use spinners for short operations (< 2 seconds expected)
- Disable interactive elements during loading to prevent duplicate submissions
- Show progress indicators for operations > 2 seconds (e.g., bulk actions in future)

### Error States (UX Patterns)

| Error Type          | Display Method                                       | User Action            |
|---------------------|------------------------------------------------------|------------------------|
| Network error       | Error banner at top of page with retry button        | Retry or refresh page  |
| Validation error    | Inline error message below form field (red text)     | Fix input, resubmit    |
| API error (4xx)     | Toast notification with error message                | Dismiss, try again     |
| API error (5xx)     | Modal dialog "Something went wrong. Please try again."| Dismiss, retry later   |
| 404 (task not found)| Empty state message "Task not found. It may have been deleted."| Return to home page    |

**Guidelines**:
- Error messages should be user-friendly (avoid technical jargon, no stack traces)
- Provide actionable recovery options (retry button, back button, dismiss)
- Log errors to console for developer debugging (structured JSON)
- Persist error messages until user dismisses or takes action

---

## Form Submission Behavior

### Form Validation (Client-Side)

- **Title**: Required, 1-200 characters, trim whitespace
- **Description**: Optional, max 2000 characters
- **Priority**: Must be one of: High, Medium, Low
- **Tags**: Max 10 tags, each max 50 characters
- **Due Date**: Optional, must be valid datetime (use browser datetime picker for input)
- **Recurrence**: Can only be set if due date is provided

**Validation Timing**:
- **On Blur**: Validate individual fields when user leaves field
- **On Submit**: Validate entire form before API call
- **Real-Time**: Show character count for title and description fields

### Form Submission Flow

1. **User Clicks Submit**:
   - Disable submit button immediately
   - Show loading spinner on button
   - Validate all fields client-side
2. **If Validation Fails**:
   - Re-enable submit button
   - Hide spinner
   - Display inline error messages
   - Focus first invalid field
3. **If Validation Passes**:
   - Make API call (POST/PUT/PATCH)
   - Keep submit button disabled during API call
4. **On API Success**:
   - Close modal/form
   - Show success toast notification
   - Refresh data (router.refresh() or refetch)
5. **On API Error**:
   - Re-enable submit button
   - Hide spinner
   - Display error message above form
   - Allow user to retry

### Optimistic UI Updates

For better perceived performance, implement optimistic updates for these actions:

| Action           | Optimistic Behavior                                  | Rollback on Error                          |
|------------------|------------------------------------------------------|--------------------------------------------|
| Mark complete    | Immediately update checkbox and task styling         | Revert checkbox, show error toast          |
| Mark incomplete  | Immediately revert checkbox and task styling         | Revert checkbox, show error toast          |
| Delete task      | Immediately remove task from list                    | Re-add task to list, show error toast      |
| Priority change  | Immediately update priority badge                    | Revert priority badge, show error toast    |

**Guidelines**:
- Only use optimistic updates for operations likely to succeed (> 95% success rate)
- Always provide visual feedback if rollback occurs (error toast + revert UI)
- Keep rollback logic simple; avoid complex state reconciliation in Phase 2

---

## Client ↔ API Interaction Rules

### API Call Structure

All frontend API calls MUST:
1. **Use Full URL**: `/api/v1/tasks` (not relative paths)
2. **Set Content-Type**: `application/json` for POST/PUT/PATCH
3. **Include Error Handling**: Catch network errors, parse error responses
4. **Log Requests**: Log API calls to console for debugging (structured JSON)

### Request Headers

```json
{
  "Content-Type": "application/json",
  "Accept": "application/json"
}
```

**Phase 2**: No authentication headers (single-user system)
**Future**: `Authorization: Bearer <token>` for JWT-based auth

### Error Response Parsing

API errors return structured JSON:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title is required",
    "details": [{ "field": "title", "issue": "Title cannot be empty" }]
  }
}
```

**Frontend Handling**:
- Parse `error.message` for user-facing display
- Use `error.details` for inline field validation errors
- Log `error.code` for debugging and error tracking

### Retry Logic

| Error Type         | Retry Strategy                                       |
|--------------------|------------------------------------------------------|
| Network timeout    | Retry up to 3 times with exponential backoff         |
| 5xx server error   | Retry once after 2 seconds                           |
| 4xx client error   | Do NOT retry (user must fix input)                   |
| Connection refused | Do NOT retry (backend is down, show error banner)    |

**Guidelines**:
- Implement retry logic only for transient errors (network timeouts, 5xx)
- Show retry attempt count to user if retrying (e.g., "Retrying... (1/3)")
- After max retries, display final error message with manual retry option

---

## Page-Specific Constraints

### Home Page Constraints

- **No Direct Database Access**: All task data fetched via `/api/v1/tasks` API
- **No Embedded Business Logic**: Filtering, sorting, pagination logic handled by backend
- **URL as Source of Truth**: Filters and pagination state stored in URL query params, not component state
- **Accessibility**: Keyboard navigation for task list, focus management for modals

### Task Detail Page Constraints

- **Single Task Fetch**: Only fetch requested task, not entire task list
- **No Embedded Updates**: Edit actions go through API, not direct state mutations
- **Breadcrumb Navigation**: Provide back button to return to task list

### Modal/Form Constraints

- **No Direct DB Writes**: All form submissions via API (POST/PUT/PATCH)
- **Controlled Components**: Use controlled inputs for forms (React state or form libraries)
- **Escape to Close**: Pressing ESC key closes modal without saving
- **Click Outside**: Clicking modal backdrop closes modal without saving (optional: show confirmation if form is dirty)

---

## Accessibility Requirements

- **Keyboard Navigation**: All interactive elements must be keyboard accessible (Tab, Enter, ESC)
- **ARIA Labels**: Use semantic HTML and ARIA labels for screen readers
- **Focus Management**: Trap focus within modals; restore focus to trigger element on close
- **Color Contrast**: Meet WCAG AA standards for text and interactive elements
- **Loading Announcements**: Use ARIA live regions to announce loading states to screen readers

---

## Performance Expectations

- **Time to First Byte (TTFB)**: < 500ms for initial page load
- **First Contentful Paint (FCP)**: < 1.5 seconds
- **Time to Interactive (TTI)**: < 3 seconds
- **API Response Handling**: Display loading indicators within 100ms of user action
- **Pagination**: Load next page in < 1 second
- **Optimistic Updates**: Apply immediately (< 50ms perceived delay)

---

## State Management

### Server State (Data from API)

- **Strategy**: Use Next.js server components for initial data fetch, client components for interactions
- **Caching**: Use Next.js built-in caching (fetch with `cache` option) or React Query for client-side caching (optional)
- **Revalidation**: Manual revalidation via `router.refresh()` after mutations

### Client State (UI State)

- **Modal Open/Close**: Component state or URL query param (e.g., `?modal=create-task`)
- **Form Input Values**: Controlled component state or form library (e.g., React Hook Form)
- **Loading Indicators**: Component state (boolean flags)
- **Error Messages**: Component state (string or error object)

**Guidelines**:
- Keep client state minimal; prefer server state for data
- Use URL query params for shareable/bookmarkable state (filters, pagination)
- Avoid global state management (Redux, Zustand) unless necessary for complex interactions (Phase 2: not needed)

---

## Browser Compatibility

- **Target Browsers**: Chrome, Firefox, Safari, Edge (last 2 major versions)
- **JavaScript Required**: Core functionality requires JavaScript (forms, modals, filtering)
- **Graceful Degradation**: Display warning banner if JavaScript is disabled
- **Mobile Responsive**: Support mobile browsers (iOS Safari, Chrome Android)

---

## Future Frontend Enhancements

Phase 3 may add:
- **Real-Time Updates**: WebSocket or Server-Sent Events for live task list updates
- **Offline Support**: Service worker for offline task creation (sync when online)
- **Drag-and-Drop**: Reorder tasks via drag-and-drop
- **Keyboard Shortcuts**: Hotkeys for quick actions (e.g., `Ctrl+N` for new task)
- **Dark Mode**: Toggle between light and dark themes
