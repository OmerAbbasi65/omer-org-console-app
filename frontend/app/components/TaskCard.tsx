'use client';

import type { Task } from '@/lib/types';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: string, completed: boolean) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
}

export function TaskCard({ task, onToggleComplete, onEdit, onDelete }: TaskCardProps) {
  const priorityColors = {
    low: 'bg-blue-100 text-blue-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-red-100 text-red-800',
  };

  return (
    <div className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3 flex-1">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={(e) => onToggleComplete(task.id, e.target.checked)}
            className="mt-1 h-5 w-5 rounded border-gray-300 text-primary focus:ring-primary"
          />
          <div className="flex-1">
            <h3
              className={`font-medium ${
                task.completed ? 'line-through text-gray-500' : 'text-gray-900'
              }`}
            >
              {task.title}
            </h3>
            {task.description && (
              <p className="text-sm text-gray-600 mt-1">{task.description}</p>
            )}
            <div className="flex items-center space-x-2 mt-2">
              <span
                className={`text-xs px-2 py-1 rounded ${
                  priorityColors[task.priority]
                }`}
              >
                {task.priority}
              </span>
              {task.tags.map((tag) => (
                <span
                  key={tag}
                  className="text-xs px-2 py-1 rounded bg-gray-100 text-gray-700"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>
        </div>
        <div className="flex space-x-2 ml-4">
          <button
            onClick={() => onEdit(task)}
            className="text-gray-600 hover:text-primary text-sm"
          >
            Edit
          </button>
          <button
            onClick={() => onDelete(task.id)}
            className="text-gray-600 hover:text-red-600 text-sm"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}
