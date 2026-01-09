# UI Behavior Specification: Next.js Frontend - Level 1

**Phase**: Phase 2 - Level 1 (Core Features)
**Framework**: Next.js 14+ (App Router)
**Date**: 2026-01-08

## Overview

This document defines the user interface behavior, component structure, and interaction patterns for the Level 1 (Core) Todo Web Application frontend.

---

## Component Architecture

### Layer Separation (Constitutional Requirement)

```
┌─────────────────────────────────────────┐
│  UI Components (app/components/)        │  ← Presentational only
├─────────────────────────────────────────┤
│  Server Actions (app/actions/)          │  ← API calls
├─────────────────────────────────────────┤
│  State Management (React hooks/context) │  ← Client state
└─────────────────────────────────────────┘
```

**Rules**:
- UI components must be stateless by default
- No direct API calls from components (use server actions)
- No business logic in components
- State lives in backend or controlled stores

---

## Page Structure

### Main Page: `app/page.tsx`

**URL**: `/`

**Layout**:
```
┌─────────────────────────────────────────┐
│  Header                                 │  ← App title
├─────────────────────────────────────────┤
│  TaskForm                               │  ← Add new task
├─────────────────────────────────────────┤
│  TaskList                               │  ← Display all tasks
│    ├─ TaskItem (repeated)              │
│    ├─ TaskItem                          │
│    └─ ...                               │
└─────────────────────────────────────────┘
```

**Responsibilities**:
- Fetch initial task list on page load
- Coordinate between TaskForm and TaskList
- Handle error states at page level

---

## Core Components

### 1. Header Component

**File**: `app/components/Header.tsx`

**Purpose**: Display application branding

**Props**: None

**Behavior**:
```tsx
export default function Header() {
  return (
    <header className="bg-blue-600 text-white py-4 px-6">
      <h1 className="text-2xl font-bold">AI-Native Todo App</h1>
      <p className="text-sm text-blue-100">Level 1 - Core Features</p>
    </header>
  );
}
```

**Visual States**:
- Default: Always visible at top of page

---

### 2. TaskForm Component

**File**: `app/components/TaskForm.tsx`

**Purpose**: Allow users to create new tasks

**Props**:
```typescript
interface TaskFormProps {
  onTaskCreated: (task: Task) => void;  // Callback after successful creation
}
```

**UI Elements**:
- Text input for task title (required)
- Textarea for task description (optional)
- "Add Task" submit button
- Error message display area

**Behavior**:

**Initial State**:
```typescript
{
  title: "",           // Empty input
  description: "",     // Empty textarea
  isSubmitting: false, // Not submitting
  error: null          // No errors
}
```

**User Interactions**:

1. **Typing in Title Input**:
   - User types → `title` state updates
   - Clear previous errors on input change
   - Validate on blur: show error if empty after user leaves field

2. **Typing in Description Textarea**:
   - User types → `description` state updates
   - Optional field, no validation

3. **Clicking "Add Task" Button**:
   - **If title is empty**: Show error "Task title cannot be empty", prevent submission
   - **If title is valid**:
     - Set `isSubmitting = true`
     - Disable submit button
     - Show loading spinner on button
     - Call server action `createTask({ title, description })`
     - **On success**:
       - Call `onTaskCreated(newTask)`
       - Clear form inputs (`title = "", description = ""`)
       - Set `isSubmitting = false`
       - Show success toast (optional)
     - **On error**:
       - Set `error = errorMessage`
       - Set `isSubmitting = false`
       - Keep form inputs (don't clear)

4. **Pressing Enter in Title Input**:
   - If `Shift+Enter`: Insert newline (if multiline)
   - If `Enter` alone: Trigger form submission (same as button click)

**Visual States**:

| State | Button Text | Button Disabled | Spinner | Error Display |
|-------|-------------|-----------------|---------|---------------|
| Default | "Add Task" | No | No | Hidden |
| Submitting | "Adding..." | Yes | Yes | Hidden |
| Error | "Add Task" | No | No | Visible (red text) |
| Success | "Add Task" | No | No | Hidden (form cleared) |

**Example JSX**:
```tsx
<form onSubmit={handleSubmit} className="bg-white p-6 shadow rounded">
  <div className="mb-4">
    <label htmlFor="title" className="block text-sm font-medium mb-2">
      Task Title *
    </label>
    <input
      id="title"
      type="text"
      value={title}
      onChange={(e) => setTitle(e.target.value)}
      onBlur={validateTitle}
      className="w-full border rounded px-3 py-2"
      placeholder="What needs to be done?"
      disabled={isSubmitting}
    />
  </div>

  <div className="mb-4">
    <label htmlFor="description" className="block text-sm font-medium mb-2">
      Description (Optional)
    </label>
    <textarea
      id="description"
      value={description}
      onChange={(e) => setDescription(e.target.value)}
      className="w-full border rounded px-3 py-2"
      placeholder="Add more details..."
      rows={3}
      disabled={isSubmitting}
    />
  </div>

  {error && (
    <div className="mb-4 text-red-600 text-sm">
      {error}
    </div>
  )}

  <button
    type="submit"
    disabled={isSubmitting}
    className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
  >
    {isSubmitting ? "Adding..." : "Add Task"}
  </button>
</form>
```

---

### 3. TaskList Component

**File**: `app/components/TaskList.tsx`

**Purpose**: Display all tasks

**Props**:
```typescript
interface TaskListProps {
  tasks: Task[];               // Array of tasks to display
  isLoading: boolean;          // Loading state
  onTaskUpdated: (task: Task) => void;   // Callback after update
  onTaskDeleted: (taskId: string) => void; // Callback after delete
}
```

**UI Elements**:
- List container
- TaskItem components (one per task)
- Empty state message
- Loading skeleton

**Behavior**:

**Rendering Logic**:
1. **If `isLoading === true`**: Show loading skeleton (3 placeholder items)
2. **If `tasks.length === 0`**: Show empty state message
3. **If `tasks.length > 0`**: Render TaskItem for each task

**Empty State**:
```tsx
<div className="text-center py-12 text-gray-500">
  <p className="text-lg">No tasks yet. Add your first task!</p>
</div>
```

**Loading State**:
```tsx
<div className="space-y-3">
  {[1, 2, 3].map((i) => (
    <div key={i} className="animate-pulse bg-gray-200 h-16 rounded" />
  ))}
</div>
```

**Task List** (with tasks):
```tsx
<div className="space-y-3">
  {tasks.map((task) => (
    <TaskItem
      key={task.id}
      task={task}
      onUpdated={onTaskUpdated}
      onDeleted={onTaskDeleted}
    />
  ))}
</div>
```

---

### 4. TaskItem Component

**File**: `app/components/TaskItem.tsx`

**Purpose**: Display and manage a single task

**Props**:
```typescript
interface TaskItemProps {
  task: Task;                        // Task data
  onUpdated: (task: Task) => void;   // Callback after update
  onDeleted: (taskId: string) => void; // Callback after delete
}
```

**UI Elements**:
- Checkbox (completion toggle)
- Task title (editable in edit mode)
- Task description (editable in edit mode)
- "Edit" button
- "Delete" button
- "Save" button (edit mode only)
- "Cancel" button (edit mode only)

**Component State**:
```typescript
{
  isEditing: false,           // Toggle edit mode
  editTitle: task.title,      // Local edit buffer
  editDescription: task.description, // Local edit buffer
  isUpdating: false,          // Async operation in progress
  isDeleting: false,          // Delete operation in progress
  showDeleteConfirm: false,   // Show delete confirmation dialog
  error: null                 // Error message
}
```

**Modes**:

#### View Mode (Default)

**Appearance**:
- Checkbox for completion status
- Task title (bold if incomplete, strikethrough if complete)
- Task description (gray text below title if present)
- "Edit" button (secondary style)
- "Delete" button (danger style)

**Interactions**:

1. **Click Checkbox**:
   - Set `isUpdating = true`
   - Call server action `toggleTaskCompletion(task.id)`
   - **On success**:
     - Update local state with toggled `completed` value
     - Call `onUpdated(updatedTask)`
     - Visual feedback: apply/remove strikethrough
   - **On error**:
     - Revert checkbox state
     - Show error toast

2. **Click "Edit" Button**:
   - Set `isEditing = true`
   - Populate `editTitle` and `editDescription` with current values
   - Focus on title input

3. **Click "Delete" Button**:
   - Set `showDeleteConfirm = true`
   - Show modal/dialog: "Are you sure you want to delete this task?"

**Example JSX (View Mode)**:
```tsx
<div className="bg-white p-4 shadow rounded flex items-start gap-4">
  <input
    type="checkbox"
    checked={task.completed}
    onChange={handleToggleComplete}
    disabled={isUpdating}
    className="mt-1"
  />

  <div className="flex-1">
    <h3 className={`font-semibold ${task.completed ? 'line-through text-gray-400' : ''}`}>
      {task.title}
    </h3>
    {task.description && (
      <p className="text-sm text-gray-600 mt-1">{task.description}</p>
    )}
  </div>

  <div className="flex gap-2">
    <button
      onClick={handleEditClick}
      className="px-3 py-1 text-sm border rounded hover:bg-gray-50"
    >
      Edit
    </button>
    <button
      onClick={handleDeleteClick}
      className="px-3 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700"
    >
      Delete
    </button>
  </div>
</div>
```

#### Edit Mode

**Appearance**:
- Checkbox (disabled in edit mode)
- Text input for title (editable)
- Textarea for description (editable)
- "Save" button (primary style)
- "Cancel" button (secondary style)
- No "Edit" or "Delete" buttons

**Interactions**:

1. **Typing in Title Input**:
   - Update `editTitle` state
   - Clear errors on change

2. **Typing in Description Textarea**:
   - Update `editDescription` state

3. **Click "Save" Button**:
   - **If editTitle is empty**: Show error "Task title cannot be empty", prevent save
   - **If valid**:
     - Set `isUpdating = true`
     - Disable inputs and buttons
     - Call server action `updateTask(task.id, { title: editTitle, description: editDescription })`
     - **On success**:
       - Set `isEditing = false`
       - Call `onUpdated(updatedTask)`
       - Exit edit mode
     - **On error**:
       - Show error message
       - Set `isUpdating = false`
       - Stay in edit mode

4. **Click "Cancel" Button**:
   - Revert `editTitle` and `editDescription` to original values
   - Set `isEditing = false`
   - Clear any errors

5. **Press Escape Key**:
   - Same as clicking "Cancel"

**Example JSX (Edit Mode)**:
```tsx
<div className="bg-white p-4 shadow rounded">
  <div className="mb-3">
    <input
      type="text"
      value={editTitle}
      onChange={(e) => setEditTitle(e.target.value)}
      className="w-full border rounded px-3 py-2"
      placeholder="Task title"
      disabled={isUpdating}
      autoFocus
    />
  </div>

  <div className="mb-3">
    <textarea
      value={editDescription}
      onChange={(e) => setEditDescription(e.target.value)}
      className="w-full border rounded px-3 py-2"
      placeholder="Description (optional)"
      rows={3}
      disabled={isUpdating}
    />
  </div>

  {error && (
    <div className="mb-3 text-red-600 text-sm">{error}</div>
  )}

  <div className="flex gap-2">
    <button
      onClick={handleSave}
      disabled={isUpdating}
      className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
    >
      {isUpdating ? "Saving..." : "Save"}
    </button>
    <button
      onClick={handleCancel}
      disabled={isUpdating}
      className="px-4 py-2 border rounded hover:bg-gray-50"
    >
      Cancel
    </button>
  </div>
</div>
```

#### Delete Confirmation Dialog

**Appearance**:
- Modal overlay (semi-transparent background)
- Centered dialog box
- Warning message: "Are you sure you want to delete this task?"
- Task title shown for context
- "Confirm" button (danger style)
- "Cancel" button (secondary style)

**Interactions**:

1. **Click "Confirm" Button**:
   - Set `isDeleting = true`
   - Disable both buttons
   - Call server action `deleteTask(task.id)`
   - **On success**:
     - Call `onDeleted(task.id)`
     - Close dialog
     - Remove TaskItem from UI
   - **On error**:
     - Show error message
     - Set `isDeleting = false`
     - Keep dialog open

2. **Click "Cancel" Button**:
   - Set `showDeleteConfirm = false`
   - Close dialog

3. **Click Outside Dialog**:
   - Same as clicking "Cancel"

4. **Press Escape Key**:
   - Same as clicking "Cancel"

**Example JSX (Delete Confirmation)**:
```tsx
{showDeleteConfirm && (
  <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div className="bg-white p-6 rounded shadow-lg max-w-md">
      <h3 className="text-lg font-semibold mb-2">Delete Task?</h3>
      <p className="text-gray-600 mb-4">
        Are you sure you want to delete "{task.title}"?
        This action cannot be undone.
      </p>

      <div className="flex gap-3 justify-end">
        <button
          onClick={handleCancelDelete}
          disabled={isDeleting}
          className="px-4 py-2 border rounded hover:bg-gray-50"
        >
          Cancel
        </button>
        <button
          onClick={handleConfirmDelete}
          disabled={isDeleting}
          className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 disabled:opacity-50"
        >
          {isDeleting ? "Deleting..." : "Delete"}
        </button>
      </div>
    </div>
  </div>
)}
```

---

## State Management

### Page-Level State (`app/page.tsx`)

```typescript
const [tasks, setTasks] = useState<Task[]>([]);
const [isLoading, setIsLoading] = useState(true);
const [error, setError] = useState<string | null>(null);

useEffect(() => {
  fetchTasks();
}, []);

async function fetchTasks() {
  setIsLoading(true);
  try {
    const result = await getTasks(); // Server action
    setTasks(result.tasks);
    setError(null);
  } catch (err) {
    setError("Failed to load tasks. Please refresh the page.");
  } finally {
    setIsLoading(false);
  }
}

// Callback handlers
function handleTaskCreated(newTask: Task) {
  setTasks([...tasks, newTask]); // Add to end of list
}

function handleTaskUpdated(updatedTask: Task) {
  setTasks(tasks.map(t => t.id === updatedTask.id ? updatedTask : t));
}

function handleTaskDeleted(taskId: string) {
  setTasks(tasks.filter(t => t.id !== taskId));
}
```

**No global state management needed for Level 1** (React state sufficient).

---

## Server Actions

**File**: `app/actions/tasks.ts`

```typescript
'use server';

import { revalidatePath } from 'next/cache';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function getTasks() {
  const res = await fetch(`${API_BASE_URL}/api/v1/tasks`, {
    cache: 'no-store' // Always fetch fresh data
  });

  if (!res.ok) {
    throw new Error('Failed to fetch tasks');
  }

  const data = await res.json();
  return data.data; // Returns { tasks: [], total: number }
}

export async function createTask(input: { title: string; description?: string }) {
  const res = await fetch(`${API_BASE_URL}/api/v1/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input)
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error?.message || 'Failed to create task');
  }

  const data = await res.json();
  revalidatePath('/');
  return data.data; // Returns Task object
}

export async function updateTask(taskId: string, input: { title?: string; description?: string }) {
  const res = await fetch(`${API_BASE_URL}/api/v1/tasks/${taskId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input)
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error?.message || 'Failed to update task');
  }

  const data = await res.json();
  revalidatePath('/');
  return data.data;
}

export async function toggleTaskCompletion(taskId: string) {
  const res = await fetch(`${API_BASE_URL}/api/v1/tasks/${taskId}/toggle`, {
    method: 'PATCH'
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error?.message || 'Failed to toggle task');
  }

  const data = await res.json();
  revalidatePath('/');
  return data.data;
}

export async function deleteTask(taskId: string) {
  const res = await fetch(`${API_BASE_URL}/api/v1/tasks/${taskId}`, {
    method: 'DELETE'
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error?.message || 'Failed to delete task');
  }

  revalidatePath('/');
}
```

---

## Error Handling

### Error Types and Responses

| Error Scenario | UI Behavior |
|----------------|-------------|
| Network failure (API unreachable) | Show error message: "Unable to connect. Please check your connection." |
| 400 Bad Request (validation error) | Show specific error from API (e.g., "Task title cannot be empty") |
| 404 Not Found (task doesn't exist) | Show error: "Task not found. It may have been deleted." |
| 500 Server Error | Show error: "Something went wrong. Please try again." |
| Timeout | Show error: "Request timed out. Please try again." |

### Error Display Patterns

1. **Inline Errors**: Show below input fields (form validation)
2. **Toast Notifications**: Show at top-right for async operation results
3. **Page-Level Errors**: Show at top of page (full red banner)

---

## Responsive Design

### Breakpoints

| Device | Viewport Width | Layout Adjustments |
|--------|----------------|-------------------|
| Mobile | 375px - 767px | Single column, full-width buttons |
| Tablet | 768px - 1023px | Single column, wider margins |
| Desktop | 1024px+ | Max-width container (768px), centered |

### Mobile Optimizations

- Larger touch targets (min 44x44px for buttons)
- Simplified delete confirmation (modal instead of inline)
- Reduced padding/margins
- Stack buttons vertically on narrow screens

---

## Accessibility (a11y)

### Requirements

1. **Keyboard Navigation**:
   - All interactive elements focusable via Tab
   - Enter key submits forms
   - Escape key closes modals

2. **Screen Reader Support**:
   - Proper ARIA labels on form inputs
   - `aria-live` regions for dynamic updates
   - Semantic HTML (`<header>`, `<main>`, `<form>`, `<button>`)

3. **Visual Indicators**:
   - Focus outlines on all interactive elements
   - Color contrast ratio ≥ 4.5:1 (WCAG AA)
   - Loading states announced to screen readers

---

## Performance Targets

- **First Contentful Paint (FCP)**: < 1.5s
- **Time to Interactive (TTI)**: < 3s
- **Task List Render**: < 100ms for 50 tasks
- **Form Submission**: < 2s (including network latency)

---

## Constitutional Compliance

This UI specification follows the Phase 2 constitution:

✅ **Next.js App Router**: Using modern App Router patterns
✅ **Layer Separation**: UI, server actions, and state clearly separated
✅ **No Direct Database Access**: All data via backend API
✅ **Stateless Components**: UI components are presentational
✅ **Progressive Features**: Only Level 1 features included
