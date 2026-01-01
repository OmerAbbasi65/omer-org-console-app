"""Incomplete command - Mark a task as incomplete"""

import argparse
from src.domain.task import get_current_timestamp
from src.storage.storage_interface import StorageInterface
from src.cli.formatter import format_task_incompleted, format_task_not_found


def execute(args: argparse.Namespace, storage: StorageInterface) -> None:
    """
    Execute the incomplete command.

    Marks an existing task as incomplete.

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

    # Mark as incomplete
    task.completed = False
    task.updatedAt = get_current_timestamp()

    # Save tasks
    storage.save_tasks(tasks)

    # Print success message
    print(format_task_incompleted(args.task_id))
