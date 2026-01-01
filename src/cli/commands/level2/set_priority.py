"""Set-priority command - Update task priority"""

import argparse
from src.domain.task import get_current_timestamp
from src.domain.validation import validate_priority
from src.storage.storage_interface import StorageInterface
from src.cli.formatter import format_success, format_task_not_found


def execute(args: argparse.Namespace, storage: StorageInterface) -> None:
    """
    Execute the set-priority command.

    Updates the priority of an existing task.

    Args:
        args: Parsed command-line arguments (task_id, priority)
        storage: Storage instance for loading/saving tasks
    """
    # Validate priority
    validate_priority(args.priority)

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

    # Update priority
    task.priority = args.priority
    task.updatedAt = get_current_timestamp()

    # Save tasks
    storage.save_tasks(tasks)

    # Print success message
    print(format_success(f"Priority set to '{args.priority}' for task {args.task_id}"))
