"""Complete command - Mark a task as complete"""

import argparse
from src.domain.task import get_current_timestamp
from src.domain.recurrence import calculate_next_due_date
from src.storage.storage_interface import StorageInterface
from src.cli.formatter import format_task_completed, format_task_not_found, format_success


def execute(args: argparse.Namespace, storage: StorageInterface) -> None:
    """
    Execute the complete command.

    Marks an existing task as complete. For recurring tasks, reschedules to next occurrence.

    Args:
        args: Parsed command-line arguments (task_id)
        storage: Storage instance for loading/saving tasks
    """
    # Load existing tasks
    tasks = storage.load_tasks()

    # Find task by ID
    task = None
    for t in tasks:
        if t.id == args.task_id:
            task = t
            break

    if task is None:
        print(format_task_not_found(args.task_id))
        return

    # Check if recurring task
    if task.recurrence != "none" and task.dueDate is not None:
        # Reschedule to next occurrence
        task.dueDate = calculate_next_due_date(task.dueDate, task.recurrence)
        task.completed = False  # Reset completion
        task.reminderTime = None  # Reset reminder
        task.lastNotified = None  # Reset notification
        task.updatedAt = get_current_timestamp()

        storage.save_tasks(tasks)
        print(format_success(f"Recurring task {args.task_id} rescheduled to {task.dueDate}"))
    else:
        # Mark as complete
        task.completed = True
        task.updatedAt = get_current_timestamp()

        storage.save_tasks(tasks)
        print(format_task_completed(args.task_id))
