'use client';

import { useState, useEffect } from 'react';
import type { Task, TaskCreate } from './lib/types';
import { api } from './lib/api';
import { TaskList } from './components/TaskList';
import { TaskForm } from './components/TaskForm';
import { Modal } from './components/Modal';
import { DeleteConfirmModal } from './components/DeleteConfirmModal';

export default function HomePage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [taskToDelete, setTaskToDelete] = useState<Task | null>(null);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.getTasks({ status: 'active' });
      setTasks(response.tasks);
    } catch (error) {
      console.error('Failed to load tasks:', error);
      setError(error instanceof Error ? error.message : 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (data: TaskCreate) => {
    try {
      await api.createTask(data);
      setIsCreateModalOpen(false);
      loadTasks();
    } catch (error) {
      console.error('Failed to create task:', error);
    }
  };

  const handleUpdateTask = async (data: TaskCreate) => {
    if (!selectedTask) return;

    try {
      await api.updateTask(selectedTask.id, data);
      setIsEditModalOpen(false);
      setSelectedTask(null);
      loadTasks();
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  const handleToggleComplete = async (id: string, completed: boolean) => {
    try {
      await api.updateTask(id, { completed });
      loadTasks();
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  const handleEdit = (task: Task) => {
    setSelectedTask(task);
    setIsEditModalOpen(true);
  };

  const handleDeleteClick = (id: string) => {
    const task = tasks.find((t) => t.id === id);
    if (task) {
      setTaskToDelete(task);
      setIsDeleteModalOpen(true);
    }
  };

  const handleDeleteConfirm = async () => {
    if (!taskToDelete) return;

    try {
      await api.deleteTask(taskToDelete.id);
      setIsDeleteModalOpen(false);
      setTaskToDelete(null);
      loadTasks();
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
        <p className="text-gray-600 mt-2">
          Manage your tasks efficiently with AI-powered assistance
        </p>
      </div>

      <div className="mb-6">
        <button
          onClick={() => setIsCreateModalOpen(true)}
          className="px-4 py-2 text-sm font-medium text-white bg-primary rounded-md hover:bg-blue-600"
        >
          + Add Task
        </button>
      </div>

      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-3">
              <div className="text-red-500 font-medium text-sm">Error</div>
              <p className="text-sm text-red-700">{error}</p>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => loadTasks()}
                className="text-sm text-red-600 hover:text-red-800 font-medium"
              >
                Retry
              </button>
              <button
                onClick={() => setError(null)}
                className="text-sm text-red-400 hover:text-red-600"
              >
                ×
              </button>
            </div>
          </div>
        </div>
      )}

      <TaskList
        tasks={tasks}
        loading={loading}
        onToggleComplete={handleToggleComplete}
        onEdit={handleEdit}
        onDelete={handleDeleteClick}
      />

      {/* Create Task Modal */}
      <Modal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        title="Create New Task"
      >
        <TaskForm
          onSubmit={handleCreateTask}
          onCancel={() => setIsCreateModalOpen(false)}
        />
      </Modal>

      {/* Edit Task Modal */}
      <Modal
        isOpen={isEditModalOpen}
        onClose={() => {
          setIsEditModalOpen(false);
          setSelectedTask(null);
        }}
        title="Edit Task"
      >
        <TaskForm
          task={selectedTask}
          onSubmit={handleUpdateTask}
          onCancel={() => {
            setIsEditModalOpen(false);
            setSelectedTask(null);
          }}
        />
      </Modal>

      {/* Delete Confirmation Modal */}
      <DeleteConfirmModal
        isOpen={isDeleteModalOpen}
        onClose={() => {
          setIsDeleteModalOpen(false);
          setTaskToDelete(null);
        }}
        onConfirm={handleDeleteConfirm}
        taskTitle={taskToDelete?.title || ''}
      />
    </div>
  );
}
