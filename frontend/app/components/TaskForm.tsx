'use client';

import { useState } from 'react';
import type { Task, TaskCreate, Priority } from '@/lib/types';

interface TaskFormProps {
  task?: Task | null;
  onSubmit: (data: TaskCreate) => void;
  onCancel: () => void;
}

export function TaskForm({ task, onSubmit, onCancel }: TaskFormProps) {
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  const [priority, setPriority] = useState<Priority>(
    (task?.priority as Priority) || 'medium'
  );
  const [titleError, setTitleError] = useState<string | null>(null);
  const [descriptionError, setDescriptionError] = useState<string | null>(null);

  const validateTitle = (value: string) => {
    if (!value.trim()) {
      setTitleError('Title is required');
      return false;
    }
    if (value.length > 200) {
      setTitleError('Title must be 200 characters or less');
      return false;
    }
    setTitleError(null);
    return true;
  };

  const validateDescription = (value: string) => {
    if (value.length > 2000) {
      setDescriptionError('Description must be 2000 characters or less');
      return false;
    }
    setDescriptionError(null);
    return true;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const isTitleValid = validateTitle(title);
    const isDescriptionValid = validateDescription(description);

    if (isTitleValid && isDescriptionValid) {
      onSubmit({
        title: title.trim(),
        description: description.trim() || null,
        priority,
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <div className="flex justify-between items-center mb-1">
          <label htmlFor="title" className="block text-sm font-medium text-gray-700">
            Title *
          </label>
          <span className={`text-xs ${title.length > 180 ? 'text-orange-500' : 'text-gray-500'}`}>
            {title.length}/200
          </span>
        </div>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            if (titleError) validateTitle(e.target.value);
          }}
          onBlur={(e) => validateTitle(e.target.value)}
          required
          maxLength={200}
          className={`mt-1 block w-full rounded-md shadow-sm focus:border-primary focus:ring-primary sm:text-sm px-3 py-2 border ${
            titleError ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="Enter task title"
        />
        {titleError && (
          <p className="mt-1 text-sm text-red-600">{titleError}</p>
        )}
      </div>

      <div>
        <div className="flex justify-between items-center mb-1">
          <label
            htmlFor="description"
            className="block text-sm font-medium text-gray-700"
          >
            Description
          </label>
          <span className={`text-xs ${description.length > 1800 ? 'text-orange-500' : 'text-gray-500'}`}>
            {description.length}/2000
          </span>
        </div>
        <textarea
          id="description"
          value={description}
          onChange={(e) => {
            setDescription(e.target.value);
            if (descriptionError) validateDescription(e.target.value);
          }}
          onBlur={(e) => validateDescription(e.target.value)}
          maxLength={2000}
          rows={3}
          className={`mt-1 block w-full rounded-md shadow-sm focus:border-primary focus:ring-primary sm:text-sm px-3 py-2 border ${
            descriptionError ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="Enter task description (optional)"
        />
        {descriptionError && (
          <p className="mt-1 text-sm text-red-600">{descriptionError}</p>
        )}
      </div>

      <div>
        <label
          htmlFor="priority"
          className="block text-sm font-medium text-gray-700"
        >
          Priority
        </label>
        <select
          id="priority"
          value={priority}
          onChange={(e) => setPriority(e.target.value as Priority)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm px-3 py-2 border"
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>

      <div className="flex justify-end space-x-3">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 text-sm font-medium text-white bg-primary rounded-md hover:bg-blue-600"
        >
          {task ? 'Update' : 'Create'} Task
        </button>
      </div>
    </form>
  );
}
