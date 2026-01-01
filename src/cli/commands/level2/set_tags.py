"""Set-tags command - Update task tags"""

import argparse
from src.domain.task import get_current_timestamp
from src.domain.validation import validate_tags
from src.storage.storage_interface import StorageInterface
from src.cli.formatter import format_success, format_task_not_found


def execute(args: argparse.Namespace, storage: StorageInterface) -> None:
    """
    Execute the set-tags command.

    Updates the tags of an existing task.

    Args:
        args: Parsed command-line arguments (task_id, tags)
        storage: Storage instance for loading/saving tasks
    """
    # Parse tags
    tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]

    # Validate tags
    validate_tags(tags)

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

    # Update tags
    task.tags = tags
    task.updatedAt = get_current_timestamp()

    # Save tasks
    storage.save_tasks(tasks)

    # Print success message
    tags_str = ", ".join(tags) if tags else "(none)"
    print(format_success(f"Tags set to [{tags_str}] for task {args.task_id}"))
