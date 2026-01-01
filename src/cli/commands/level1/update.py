"""Update command - Modify an existing task"""

import argparse
from src.domain.task import get_current_timestamp
from src.domain.validation import validate_task_update
from src.storage.storage_interface import StorageInterface
from src.cli.formatter import format_task_updated, format_task_not_found, format_error


def execute(args: argparse.Namespace, storage: StorageInterface) -> None:
    """
    Execute the update command.

    Updates title and/or description of an existing task.

    Args:
        args: Parsed command-line arguments (task_id, title, description)
        storage: Storage instance for loading/saving tasks
    """
    # Validate at least one field is being updated
    if args.title is None and args.description is None:
        print(format_error("At least one field (--title or --description) must be provided"))
        return

    # Validate the update fields
    validate_task_update(title=args.title, description=args.description)

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

    # Update fields
    if args.title is not None:
        task.title = args.title

    if args.description is not None:
        task.description = args.description

    # Update timestamp
    task.updatedAt = get_current_timestamp()

    # Save tasks
    storage.save_tasks(tasks)

    # Print success message
    print(format_task_updated(args.task_id))
