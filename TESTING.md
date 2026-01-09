# Phase 2 Level 1 - Testing Guide

This guide provides a comprehensive checklist for testing all Level 1 (Core) features of the Todo Web Application.

## Prerequisites

Before testing, ensure:
- ✅ Backend is running on http://localhost:8000
- ✅ Frontend is running on http://localhost:3000
- ✅ Neon database is configured and connected
- ✅ Database tables are created (check logs on backend startup)

## Testing Checklist

### 1. Initial Load

**Test**: Open the application for the first time

**Steps**:
1. Open http://localhost:3000 in your browser
2. Wait for page to load

**Expected Results**:
- ✅ Page loads within 2 seconds
- ✅ Header displays "AI-Native Todo App" and "Level 1 - Core Features"
- ✅ Task form is visible with title and description inputs
- ✅ "Add Task" button is visible
- ✅ Empty state message displays: "No tasks yet. Add your first task!"
- ✅ No errors in browser console

**User Story**: User Story 2 - View Task List, Scenario 2

---

### 2. Create Task (Basic)

**Test**: Add a task with only a title

**Steps**:
1. Type "Buy groceries" in the title input
2. Leave description empty
3. Click "Add Task" button

**Expected Results**:
- ✅ Button shows "Adding..." while submitting
- ✅ Task appears in the list within 2 seconds
- ✅ Task displays with:
  - Empty checkbox (uncompleted)
  - Title: "Buy groceries"
  - No description
  - "Edit" button
  - "Delete" button
- ✅ Input fields are cleared after creation
- ✅ Empty state message disappears

**User Story**: User Story 1 - Add New Task, Scenario 1

---

### 3. Create Task (With Description)

**Test**: Add a task with title and description

**Steps**:
1. Type "Finish project report" in the title input
2. Type "Complete introduction, methodology, and results sections" in description
3. Click "Add Task"

**Expected Results**:
- ✅ Task appears in the list
- ✅ Task displays with:
  - Title: "Finish project report"
  - Description: "Complete introduction, methodology, and results sections"
  - Uncompleted status

**User Story**: User Story 1 - Add New Task, Scenario 2

---

### 4. Create Task (Validation Error)

**Test**: Try to add a task with empty title

**Steps**:
1. Leave title input empty (or only whitespace)
2. Click "Add Task"

**Expected Results**:
- ✅ Error message displays: "Task title cannot be empty"
- ✅ No task is created
- ✅ Error is red text below form fields
- ✅ Button is not disabled

**User Story**: User Story 1 - Add New Task, Scenario 3

**Edge Case**: Empty title validation

---

### 5. View Multiple Tasks

**Test**: Display multiple tasks in the list

**Steps**:
1. Create 3-5 more tasks with different titles

**Expected Results**:
- ✅ All tasks are displayed in the list
- ✅ Tasks are ordered with newest at the top
- ✅ Each task shows ID, title, completion status, and action buttons
- ✅ No performance lag with 5+ tasks

**User Story**: User Story 2 - View Task List, Scenario 1

---

### 6. Mark Task as Complete

**Test**: Toggle task completion status

**Steps**:
1. Locate "Buy groceries" task
2. Click the checkbox next to it

**Expected Results**:
- ✅ Checkbox becomes checked
- ✅ Task title gets strikethrough styling
- ✅ Task title appears in gray color
- ✅ Update persists (refresh page to verify)

**User Story**: User Story 4 - Mark Task Complete/Incomplete, Scenario 1

---

### 7. Mark Task as Incomplete

**Test**: Uncheck a completed task

**Steps**:
1. Click the checkbox of a completed task

**Expected Results**:
- ✅ Checkbox becomes unchecked
- ✅ Strikethrough styling is removed
- ✅ Task title returns to normal black color
- ✅ Update persists

**User Story**: User Story 4 - Mark Task Complete/Incomplete, Scenario 2

---

### 8. Update Task Title

**Test**: Edit a task's title

**Steps**:
1. Click "Edit" button on "Buy groceries" task
2. Change title to "Buy groceries and fruits"
3. Click "Save"

**Expected Results**:
- ✅ Task enters edit mode with input fields
- ✅ Title input is focused and pre-filled
- ✅ Description textarea is pre-filled (if exists)
- ✅ "Save" and "Cancel" buttons appear
- ✅ "Edit" and "Delete" buttons disappear
- ✅ After save, task displays new title
- ✅ Edit mode exits automatically
- ✅ Update persists

**User Story**: User Story 3 - Update Task, Scenario 1

---

### 9. Update Task Description

**Test**: Edit a task's description

**Steps**:
1. Click "Edit" on "Finish project report"
2. Change description to "Complete all sections including conclusion"
3. Click "Save"

**Expected Results**:
- ✅ Task shows updated description
- ✅ Edit mode exits
- ✅ Update persists

**User Story**: User Story 3 - Update Task, Scenario 2

---

### 10. Update Task (Validation Error)

**Test**: Try to save empty title during edit

**Steps**:
1. Click "Edit" on any task
2. Clear the title field completely
3. Click "Save"

**Expected Results**:
- ✅ Error message displays: "Task title cannot be empty"
- ✅ Task is NOT updated
- ✅ Edit mode stays active
- ✅ Error is red text below inputs

**User Story**: User Story 3 - Update Task, Scenario 3

**Edge Case**: Empty title validation during update

---

### 11. Cancel Edit

**Test**: Cancel editing without saving changes

**Steps**:
1. Click "Edit" on any task
2. Change title to something different
3. Click "Cancel"

**Expected Results**:
- ✅ Task reverts to original title (no changes saved)
- ✅ Edit mode exits
- ✅ No error messages

**User Story**: User Story 3 - Update Task, Scenario 4

---

### 12. Delete Task (Cancel)

**Test**: Cancel task deletion

**Steps**:
1. Click "Delete" button on any task
2. In the confirmation dialog, click "Cancel"

**Expected Results**:
- ✅ Confirmation dialog appears with message: "Are you sure you want to delete [task title]?"
- ✅ Dialog shows task title for context
- ✅ Dialog has "Confirm" (red) and "Cancel" buttons
- ✅ After clicking "Cancel", dialog closes
- ✅ Task remains in the list (not deleted)

**User Story**: User Story 5 - Delete Task, Scenario 3

---

### 13. Delete Task (Confirm)

**Test**: Permanently delete a task

**Steps**:
1. Click "Delete" button on "Buy groceries and fruits"
2. In the confirmation dialog, click "Confirm"

**Expected Results**:
- ✅ Button shows "Deleting..." while processing
- ✅ Dialog closes after deletion
- ✅ Task is removed from the list
- ✅ Deletion persists (refresh page to verify)

**User Story**: User Story 5 - Delete Task, Scenarios 1-2

---

### 14. Keyboard Navigation

**Test**: Use keyboard for form submission

**Steps**:
1. Type "Call dentist" in title input
2. Press **Enter** key (instead of clicking button)

**Expected Results**:
- ✅ Task is created (same as clicking "Add Task")
- ✅ Form is submitted on Enter keypress

---

### 15. Escape Key (Edit Mode)

**Test**: Press Escape to cancel edit

**Steps**:
1. Click "Edit" on any task
2. Make changes to title
3. Press **Escape** key

**Expected Results**:
- ✅ Edit mode exits without saving
- ✅ Changes are discarded

---

### 16. Escape Key (Delete Dialog)

**Test**: Press Escape to close delete confirmation

**Steps**:
1. Click "Delete" on any task
2. Press **Escape** key

**Expected Results**:
- ✅ Delete confirmation dialog closes
- ✅ Task is not deleted

---

### 17. Persistence Test

**Test**: Verify data persists across page refreshes

**Steps**:
1. Note the current tasks in the list
2. Refresh the browser page (F5 or Ctrl+R)

**Expected Results**:
- ✅ All tasks reload with correct data
- ✅ Completion statuses are preserved
- ✅ Task order is preserved
- ✅ No data loss

**Success Criteria**: SC-004 - 100% of tasks persisted

---

### 18. Loading States

**Test**: Verify loading indicators appear

**Steps**:
1. Refresh page and observe initial load
2. Add a task and observe button state
3. Toggle completion and observe
4. Edit a task and observe

**Expected Results**:
- ✅ Initial page load shows 3 gray loading skeleton boxes
- ✅ "Add Task" button shows "Adding..." during submission
- ✅ Buttons are disabled during async operations
- ✅ No UI freezing or unresponsive states

---

### 19. Error Handling (Backend Down)

**Test**: Frontend behavior when backend is unreachable

**Steps**:
1. Stop the backend server (Ctrl+C in backend terminal)
2. Refresh the frontend page
3. Try to add a task

**Expected Results**:
- ✅ Error message displays: "Failed to load tasks. Please refresh the page."
- ✅ Error banner is visible at top of page
- ✅ Attempting to add task shows error: "Failed to create task" or "Unable to connect"
- ✅ No application crash
- ✅ Error messages are user-friendly

**Edge Case**: Network failure handling

---

### 20. Responsive Design (Mobile)

**Test**: Application works on mobile viewport

**Steps**:
1. Open browser DevTools (F12)
2. Toggle device toolbar (responsive design mode)
3. Select iPhone or Android device (375px width)
4. Test all features

**Expected Results**:
- ✅ Layout adapts to narrow screen
- ✅ All buttons are tappable (min 44x44px touch targets)
- ✅ Text is readable without zooming
- ✅ Form inputs are usable
- ✅ Delete confirmation dialog is centered and readable

**Success Criteria**: SC-007 - Fully responsive UI

---

### 21. Performance Test

**Test**: Application handles 50+ tasks

**Steps**:
1. Create 50+ tasks (can use Neon SQL Editor to bulk insert)
2. Observe rendering performance
3. Test all CRUD operations

**Expected SQL for bulk insert**:
```sql
INSERT INTO tasks (id, title, description, completed, created_at, updated_at)
SELECT
  gen_random_uuid(),
  'Task ' || generate_series,
  'Description for task ' || generate_series,
  false,
  CURRENT_TIMESTAMP,
  CURRENT_TIMESTAMP
FROM generate_series(1, 50);
```

**Expected Results**:
- ✅ Task list renders within 100ms
- ✅ No scrolling lag
- ✅ CRUD operations remain fast (< 2s)
- ✅ No browser memory issues

**Success Criteria**: SC-005 - Support 1,000+ tasks without degradation

---

### 22. Database Verification

**Test**: Verify data in Neon PostgreSQL

**Steps**:
1. Go to https://console.neon.tech
2. Select your project
3. Open SQL Editor
4. Run: `SELECT * FROM tasks ORDER BY created_at DESC;`

**Expected Results**:
- ✅ All tasks from frontend are present in database
- ✅ IDs are valid UUIDs
- ✅ Timestamps are in UTC
- ✅ Completed status matches frontend
- ✅ No data corruption

---

## Test Summary

After completing all tests, verify:

### Feature Completeness
- ✅ Add tasks (with/without description)
- ✅ View all tasks
- ✅ Update task title and description
- ✅ Toggle task completion
- ✅ Delete tasks with confirmation

### Quality Checks
- ✅ Input validation works correctly
- ✅ Error messages are clear and helpful
- ✅ Loading states provide feedback
- ✅ Data persists across refreshes
- ✅ Responsive on mobile, tablet, desktop
- ✅ Keyboard navigation works
- ✅ Performance is acceptable (< 2s operations)

### Edge Cases
- ✅ Empty title validation (create & update)
- ✅ Backend unavailable handling
- ✅ Concurrent operations (multiple tabs)
- ✅ Large datasets (50+ tasks)

## Reporting Issues

If any test fails, document:
1. **Test Name**: Which test failed?
2. **Steps**: What did you do?
3. **Expected**: What should have happened?
4. **Actual**: What actually happened?
5. **Console Errors**: Any errors in browser console?
6. **Backend Logs**: Any errors in backend terminal?

## Next Steps After Testing

Once all tests pass:
- ✅ Phase 2 Level 1 is **COMPLETE**
- ✅ Ready to plan Level 2 (Organization) features
- ✅ System is validated and extensible

## Constitutional Compliance

This testing checklist validates:
- ✅ All Level 1 user stories and acceptance scenarios
- ✅ Success criteria from spec (SC-001 through SC-007)
- ✅ Edge cases from spec
- ✅ Non-functional requirements (NFR-001 through NFR-008)
