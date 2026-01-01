"""Delete command - Remove a task"""

import argparse
from src.storage.storage_interface import StorageInterface
from src.cli.formatter import format_task_deleted, format_task_not_found


def execute(args: argparse.Namespace, storage: StorageInterface) -> None:
    """
    Execute the delete command.

    Permanently removes a task from storage.

    Args:
        args: Parsed command-line arguments (task_id)
        storage: Storage instance for loading/saving tasks
    """
    # Load existing tasks
    tasks = storage.load_tasks()

    # Find task by ID
    task_index = None
    for i, t in enumerate(tasks):
        if t.id == args.task_id:
            task_index = i
            break

    if task_index is None:
        print(format_task_not_found(args.task_id))
        return

    # Remove task from list
    tasks.pop(task_index)

    # Save tasks
    storage.save_tasks(tasks)

    # Print success message
    print(format_task_deleted(args.task_id))
