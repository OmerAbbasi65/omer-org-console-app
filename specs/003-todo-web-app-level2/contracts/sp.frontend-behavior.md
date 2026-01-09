# Frontend Behavior Specification: Level 2 (Organization)

**Phase**: Phase 2 - Level 2 (Organization Features)
**Framework**: Next.js 14+ (App Router)
**Date**: 2026-01-09

## Overview

This document defines frontend behavior extensions for Level 2 (Organization) features. All Level 1 behaviors remain unchanged and fully functional.

---

## Component Extensions

### 1. TaskForm Component (Extended)

**File**: `app/components/TaskForm.tsx`

**New UI Elements** (Level 2):
- Priority selector (dropdown or button group)
- Tag input field (comma-separated or chip input)

**Component State** (Level 2 additions):

```typescript
{
  // Level 1 fields (unchanged)
  title: "",
  description: "",
  isSubmitting: false,
  error: null,

  // Level 2 fields (NEW)
  priority: null,           // "high" | "medium" | "low" | null
  tags: [],                 // string[]
  tagInput: "",             // temporary input for tag entry
  tagError: null            // validation error for tags
}
```

**New User Interactions**:

#### Priority Selection

1. **Selecting Priority**:
   - User clicks priority dropdown or button
   - Options: "No Priority" (default), "High", "Medium", "Low"
   - Selected priority updates state immediately
   - Visual feedback: selected option highlighted

2. **Visual Representation**:
   - **High**: Red badge or text
   - **Medium**: Yellow/Orange badge or text
   - **Low**: Green/Blue badge or text
   - **No Priority**: Gray text or no badge

#### Tag Entry

1. **Adding Tags (Comma-Separated)**:
   - User types "work, urgent" in tag input
   - On blur or Enter key: parse tags by comma
   - Trim whitespace from each tag
   - Deduplicate tags (case-sensitive)
   - Display as chips/badges below input
   - Clear tag input field

2. **Adding Tags (Chip Input Alternative)**:
   - User types "work" and presses Enter or comma
   - Tag immediately appears as chip
   - Input field remains focused for next tag
   - Limit: 20 tags max

3. **Removing Tags**:
   - User clicks X icon on tag chip
   - Tag is removed from array immediately

4. **Tag Validation**:
   - If tag exceeds 50 characters: show error "Tag too long (max 50 characters)"
   - If 20 tags already exist: show error "Maximum 20 tags allowed"
   - If tag is empty/whitespace: ignore silently

**Form Submission** (Level 2):

```typescript
async function handleSubmit(e: React.FormEvent) {
  e.preventDefault();

  // Level 1 validation (unchanged)
  if (!validateTitle()) {
    return;
  }

  // Level 2 validation (NEW)
  if (tags.length > 20) {
    setTagError("Maximum 20 tags allowed");
    return;
  }

  setIsSubmitting(true);
  setError(null);
  setTagError(null);

  try {
    const newTask = await createTask({
      title: title.trim(),
      description: description.trim() || undefined,
      priority: priority,        // NEW
      tags: tags                 // NEW
    });

    // Success: clear all fields including Level 2
    setTitle('');
    setDescription('');
    setPriority(null);
    setTags([]);
    onTaskCreated(newTask);
  } catch (err) {
    setError(err instanceof Error ? err.message : 'Failed to create task');
  } finally {
    setIsSubmitting(false);
  }
}
```

**Example JSX** (Level 2 additions):

```tsx
<form onSubmit={handleSubmit} className="bg-white p-6 shadow rounded">
  {/* Level 1 fields: title and description (unchanged) */}

  {/* Priority Selector (NEW) */}
  <div className="mb-4">
    <label htmlFor="priority" className="block text-sm font-medium mb-2">
      Priority (Optional)
    </label>
    <select
      id="priority"
      value={priority || ''}
      onChange={(e) => setPriority(e.target.value || null)}
      className="w-full border rounded px-3 py-2"
      disabled={isSubmitting}
    >
      <option value="">No Priority</option>
      <option value="high">High</option>
      <option value="medium">Medium</option>
      <option value="low">Low</option>
    </select>
  </div>

  {/* Tag Input (NEW) */}
  <div className="mb-4">
    <label htmlFor="tags" className="block text-sm font-medium mb-2">
      Tags (Optional)
    </label>
    <input
      id="tags"
      type="text"
      value={tagInput}
      onChange={(e) => setTagInput(e.target.value)}
      onBlur={handleTagsBlur}
      onKeyDown={handleTagsKeyDown}
      className="w-full border rounded px-3 py-2"
      placeholder="work, urgent (comma-separated)"
      disabled={isSubmitting}
    />

    {/* Tag Chips Display */}
    {tags.length > 0 && (
      <div className="flex flex-wrap gap-2 mt-2">
        {tags.map((tag, index) => (
          <span
            key={index}
            className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm flex items-center gap-1"
          >
            {tag}
            <button
              type="button"
              onClick={() => handleRemoveTag(index)}
              className="text-blue-600 hover:text-blue-800"
            >
              ×
            </button>
          </span>
        ))}
      </div>
    )}

    {tagError && (
      <div className="text-red-600 text-sm mt-1">{tagError}</div>
    )}
  </div>

  {/* Submit button (unchanged) */}
</form>
```

---

### 2. TaskItem Component (Extended)

**File**: `app/components/TaskItem.tsx`

**New Visual Elements** (Level 2):
- Priority badge (colored indicator)
- Tags displayed as inline chips

**Component State** (Level 2 additions):

```typescript
{
  // Level 1 fields (unchanged)
  isEditing: false,
  editTitle: task.title,
  editDescription: task.description || '',
  isUpdating: false,
  isDeleting: false,
  showDeleteConfirm: false,
  error: null,

  // Level 2 fields (NEW)
  editPriority: task.priority,
  editTags: task.tags,
  tagInput: ""
}
```

**View Mode** (Level 2 additions):

```tsx
<div className="bg-white p-4 shadow rounded flex items-start gap-4">
  {/* Checkbox (Level 1, unchanged) */}

  <div className="flex-1">
    {/* Priority Badge (NEW) */}
    {task.priority && (
      <span className={`
        inline-block px-2 py-1 rounded text-xs font-semibold mr-2
        ${task.priority === 'high' ? 'bg-red-100 text-red-800' : ''}
        ${task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' : ''}
        ${task.priority === 'low' ? 'bg-green-100 text-green-800' : ''}
      `}>
        {task.priority.toUpperCase()}
      </span>
    )}

    {/* Title (Level 1, unchanged) */}
    <h3 className={`font-semibold ${task.completed ? 'line-through text-gray-400' : ''}`}>
      {task.title}
    </h3>

    {/* Description (Level 1, unchanged) */}
    {task.description && (
      <p className="text-sm text-gray-600 mt-1">{task.description}</p>
    )}

    {/* Tags (NEW) */}
    {task.tags.length > 0 && (
      <div className="flex flex-wrap gap-2 mt-2">
        {task.tags.map((tag, index) => (
          <span
            key={index}
            className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs"
          >
            {tag}
          </span>
        ))}
      </div>
    )}
  </div>

  {/* Edit and Delete buttons (Level 1, unchanged) */}
</div>
```

**Edit Mode** (Level 2 additions):

- Priority selector (same as TaskForm)
- Tag input (same as TaskForm)
- Save button updates priority and tags

---

### 3. TaskList Component (Extended)

**File**: `app/components/TaskList.tsx`

**New Props** (Level 2):

```typescript
interface TaskListProps {
  tasks: Task[];
  isLoading: boolean;
  onTaskUpdated: (task: Task) => void;
  onTaskDeleted: (taskId: string) => void;

  // Level 2 props (NEW)
  filters: FilterState;       // Active filters
  onFilterChange: (filters: FilterState) => void;
  sortBy: SortField;
  sortOrder: 'asc' | 'desc';
  onSortChange: (field: SortField, order: 'asc' | 'desc') => void;
}
```

**No changes to rendering logic** (TaskItem handles Level 2 display).

---

### 4. FilterPanel Component (NEW)

**File**: `app/components/FilterPanel.tsx`

**Purpose**: Provide UI controls for filtering and sorting tasks

**UI Elements**:
- Status filter (radio buttons or dropdown)
- Priority filter (checkboxes or dropdown)
- Tag filter (multi-select or chip input)
- Sort dropdown
- "Clear Filters" button

**Component State**:

```typescript
{
  statusFilter: null,          // "completed" | "incomplete" | null
  priorityFilter: null,        // "high" | "medium" | "low" | "none" | null
  tagFilters: [],              // string[] (selected tags)
  sortBy: "createdAt",         // "priority" | "title" | "createdAt" | "updatedAt"
  sortOrder: "desc"            // "asc" | "desc"
}
```

**User Interactions**:

1. **Selecting Status Filter**:
   - User selects "Incomplete" radio button
   - `statusFilter` updates to "incomplete"
   - Trigger `onFilterChange({ ...filters, status: "incomplete" })`

2. **Selecting Priority Filter**:
   - User selects "High" from dropdown
   - `priorityFilter` updates to "high"
   - Trigger `onFilterChange({ ...filters, priority: "high" })`

3. **Selecting Tag Filters**:
   - User types "work" in tag filter input
   - User presses Enter or clicks "Add"
   - Tag "work" is added to `tagFilters` array
   - Trigger `onFilterChange({ ...filters, tags: ["work"] })`
   - Multiple tags can be added (AND logic)

4. **Changing Sort**:
   - User selects "Priority (High to Low)" from sort dropdown
   - `sortBy` updates to "priority", `sortOrder` updates to "desc"
   - Trigger `onSortChange("priority", "desc")`

5. **Clearing Filters**:
   - User clicks "Clear Filters" button
   - All filters reset to default (null, empty arrays)
   - Trigger `onFilterChange({ status: null, priority: null, tags: [], search: null })`

**Example JSX**:

```tsx
<div className="bg-white p-4 shadow rounded mb-6">
  <h3 className="text-lg font-semibold mb-4">Filters & Sort</h3>

  {/* Status Filter */}
  <div className="mb-4">
    <label className="block text-sm font-medium mb-2">Status</label>
    <select
      value={statusFilter || ''}
      onChange={(e) => handleStatusChange(e.target.value || null)}
      className="w-full border rounded px-3 py-2"
    >
      <option value="">All</option>
      <option value="incomplete">Incomplete</option>
      <option value="completed">Completed</option>
    </select>
  </div>

  {/* Priority Filter */}
  <div className="mb-4">
    <label className="block text-sm font-medium mb-2">Priority</label>
    <select
      value={priorityFilter || ''}
      onChange={(e) => handlePriorityChange(e.target.value || null)}
      className="w-full border rounded px-3 py-2"
    >
      <option value="">All</option>
      <option value="high">High</option>
      <option value="medium">Medium</option>
      <option value="low">Low</option>
      <option value="none">No Priority</option>
    </select>
  </div>

  {/* Tag Filter */}
  <div className="mb-4">
    <label className="block text-sm font-medium mb-2">Tags</label>
    <input
      type="text"
      value={tagInput}
      onChange={(e) => setTagInput(e.target.value)}
      onKeyDown={handleTagKeyDown}
      placeholder="Filter by tag (press Enter)"
      className="w-full border rounded px-3 py-2"
    />
    {tagFilters.length > 0 && (
      <div className="flex flex-wrap gap-2 mt-2">
        {tagFilters.map((tag, index) => (
          <span key={index} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm flex items-center gap-1">
            {tag}
            <button onClick={() => handleRemoveTagFilter(index)}>×</button>
          </span>
        ))}
      </div>
    )}
  </div>

  {/* Sort */}
  <div className="mb-4">
    <label className="block text-sm font-medium mb-2">Sort By</label>
    <select
      value={`${sortBy}-${sortOrder}`}
      onChange={(e) => handleSortChange(e.target.value)}
      className="w-full border rounded px-3 py-2"
    >
      <option value="createdAt-desc">Created Date (Newest First)</option>
      <option value="createdAt-asc">Created Date (Oldest First)</option>
      <option value="priority-desc">Priority (High to Low)</option>
      <option value="priority-asc">Priority (Low to High)</option>
      <option value="title-asc">Title (A-Z)</option>
      <option value="title-desc">Title (Z-A)</option>
      <option value="updatedAt-desc">Recently Updated</option>
    </select>
  </div>

  {/* Clear Filters Button */}
  <button
    onClick={handleClearFilters}
    className="w-full bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300"
  >
    Clear All Filters
  </button>
</div>
```

---

### 5. SearchBar Component (NEW)

**File**: `app/components/SearchBar.tsx`

**Purpose**: Provide search input with debounce

**Component State**:

```typescript
{
  searchTerm: "",      // Local input state
  debouncedSearch: ""  // Debounced value sent to API
}
```

**User Interactions**:

1. **Typing in Search Input**:
   - User types "groceries"
   - `searchTerm` updates immediately (for UI responsiveness)
   - After 500ms of no typing, `debouncedSearch` updates
   - Trigger `onSearchChange(debouncedSearch)`

2. **Clearing Search**:
   - User clears input or clicks X icon
   - `searchTerm` and `debouncedSearch` both reset to ""
   - Trigger `onSearchChange("")`

**Debounce Implementation**:

```typescript
import { useState, useEffect } from 'react';

function useDebounce(value: string, delay: number) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

export default function SearchBar({ onSearchChange }: { onSearchChange: (search: string) => void }) {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearch = useDebounce(searchTerm, 500);

  useEffect(() => {
    onSearchChange(debouncedSearch);
  }, [debouncedSearch]);

  return (
    <div className="relative mb-6">
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search tasks..."
        className="w-full border rounded px-4 py-2 pr-10"
      />
      {searchTerm && (
        <button
          onClick={() => setSearchTerm('')}
          className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
        >
          ×
        </button>
      )}
    </div>
  );
}
```

---

## Page-Level State Management (Level 2)

### Main Page: `app/page.tsx` (Extended)

**Page State** (Level 2 additions):

```typescript
{
  // Level 1 state (unchanged)
  tasks: Task[],
  isLoading: boolean,
  error: string | null,

  // Level 2 state (NEW)
  filters: {
    status: "completed" | "incomplete" | null,
    priority: "high" | "medium" | "low" | "none" | null,
    tags: string[],
    search: string | null
  },
  sort: {
    by: "priority" | "title" | "createdAt" | "updatedAt",
    order: "asc" | "desc"
  }
}
```

**Data Fetching** (Level 2):

```typescript
const fetchTasks = async () => {
  setIsLoading(true);
  try {
    // Build query parameters from filters and sort
    const params = new URLSearchParams();

    if (filters.status) params.append('status', filters.status);
    if (filters.priority) params.append('priority', filters.priority);
    filters.tags.forEach(tag => params.append('tag', tag));
    if (filters.search) params.append('search', filters.search);
    params.append('sortBy', sort.by);
    params.append('order', sort.order);

    const result = await getTasks(params.toString());
    setTasks(result.tasks);
    setError(null);
  } catch (err) {
    setError('Failed to load tasks. Please refresh the page.');
  } finally {
    setIsLoading(false);
  }
};

// Re-fetch when filters or sort change
useEffect(() => {
  fetchTasks();
}, [filters, sort]);
```

**Callback Handlers** (Level 2 additions):

```typescript
const handleFilterChange = (newFilters: FilterState) => {
  setFilters(newFilters);
  // fetchTasks() will be triggered by useEffect
};

const handleSortChange = (field: SortField, order: 'asc' | 'desc') => {
  setSort({ by: field, order });
  // fetchTasks() will be triggered by useEffect
};

const handleSearchChange = (searchTerm: string) => {
  setFilters({ ...filters, search: searchTerm || null });
  // fetchTasks() will be triggered by useEffect
};
```

---

## Server Actions (Level 2 Extensions)

**File**: `app/actions/tasks.ts`

### getTasks (Extended)

```typescript
export async function getTasks(queryParams?: string): Promise<TaskListResponse> {
  const url = queryParams
    ? `${API_BASE_URL}/api/v1/tasks?${queryParams}`
    : `${API_BASE_URL}/api/v1/tasks`;

  const res = await fetch(url, {
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error('Failed to fetch tasks');
  }

  const data: ApiResponse<TaskListResponse> = await res.json();

  if (!data.success || !data.data) {
    throw new Error('Invalid response from server');
  }

  return data.data;
}
```

### createTask (Extended)

No changes to signature, but now accepts `priority` and `tags`:

```typescript
export async function createTask(input: TaskCreate): Promise<Task> {
  // input.priority and input.tags are now included
  // Rest of implementation unchanged
}
```

---

## Loading States (Level 2)

### Filter Application Loading

When filters/sort change:
- Tasks list shows loading skeleton
- Filter panel remains interactive (not disabled)
- Previous tasks fade out with opacity animation

### Search Debounce Loading

During debounce period (500ms):
- No loading indicator (feels instant)
- After debounce, show loading skeleton if fetching

---

## Error Handling (Level 2)

### Filter/Sort Errors

**Invalid Query Parameters**:
- Display error: "Invalid filter selection. Please try again."
- Reset filters to default
- Log error to console

**No Results**:
- Display message: "No tasks match the selected filters."
- Show "Clear Filters" button prominently

### Tag Validation Errors

**Tag Too Long**:
- Show error below tag input: "Tag exceeds 50 character limit"
- Highlight input field in red
- Do not add tag to list

**Too Many Tags**:
- Show error: "Maximum 20 tags allowed"
- Disable tag input until user removes tags

---

## Responsive Design (Level 2)

### Mobile Adjustments

**Filter Panel**:
- Collapsible on mobile (accordion or modal)
- "Filters" button in header to toggle panel
- Full-width on mobile, sidebar on desktop

**Tag Chips**:
- Wrap to multiple lines on narrow screens
- Smaller font size on mobile (10px instead of 12px)

**Priority Badges**:
- Shorter labels on mobile ("H", "M", "L" instead of "HIGH", "MEDIUM", "LOW")

---

## Accessibility (Level 2)

### Filter Panel

- All dropdowns keyboard navigable
- Clear focus indicators
- ARIA labels: `aria-label="Filter by status"`

### Tag Input

- `aria-label="Add tags (comma-separated)"`
- Tag remove buttons: `aria-label="Remove tag [tag-name]"`

### Priority Selector

- `aria-label="Select task priority"`
- Options clearly labeled

---

## Performance Optimizations (Level 2)

### Debounce Search

- 500ms delay prevents excessive API calls
- Cancel in-flight requests if new search starts

### Memoization

```typescript
import { useMemo } from 'react';

// Memoize filter/sort state to avoid unnecessary re-renders
const filterSortKey = useMemo(
  () => JSON.stringify({ filters, sort }),
  [filters, sort]
);
```

### Virtual Scrolling (Optional)

Not required for Level 2 (1000 tasks max), but consider for Level 3.

---

## URL Query Parameters (Optional - Level 2)

**Behavior**: Update URL with current filters/sort for shareability

**Example URL**:
```
http://localhost:3000/?status=incomplete&priority=high&tag=work&sortBy=priority&order=desc
```

**Implementation**:

```typescript
import { useRouter, useSearchParams } from 'next/navigation';

// Read from URL on mount
const searchParams = useSearchParams();
const initialFilters = {
  status: searchParams.get('status'),
  priority: searchParams.get('priority'),
  tags: searchParams.getAll('tag'),
  search: searchParams.get('search')
};

// Update URL when filters change
const router = useRouter();
const updateURL = (filters: FilterState, sort: SortState) => {
  const params = new URLSearchParams();
  if (filters.status) params.set('status', filters.status);
  if (filters.priority) params.set('priority', filters.priority);
  filters.tags.forEach(tag => params.append('tag', tag));
  if (filters.search) params.set('search', filters.search);
  params.set('sortBy', sort.by);
  params.set('order', sort.order);

  router.push(`/?${params.toString()}`, { scroll: false });
};
```

---

## Constitutional Compliance

✅ **Level 1 Compatibility**: All Level 1 behaviors unchanged
✅ **No Direct Database Access**: All data via backend API
✅ **Stateless Components**: UI components are presentational
✅ **Server Actions**: All API calls via server actions
✅ **Progressive Enhancement**: Level 2 features add functionality without breaking Level 1
