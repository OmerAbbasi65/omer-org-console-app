"""Add command - Create a new task"""

import argparse
from src.domain.task import create_task
from src.storage.storage_interface import StorageInterface
from src.cli.formatter import format_task_created


def execute(args: argparse.Namespace, storage: StorageInterface) -> None:
    """
    Execute the add command.

    Creates a new task with the provided title and optional description, priority, tags.

    Args:
        args: Parsed command-line arguments (title, description, priority, tags)
        storage: Storage instance for persisting tasks
    """
    # Parse tags if provided
    tags = None
    if hasattr(args, "tags") and args.tags is not None:
        tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]

    # Get Level 2/3 fields if provided
    priority = getattr(args, "priority", None)
    dueDate = getattr(args, "due", None)
    recurrence = getattr(args, "recurrence", "none")
    reminderTime = getattr(args, "remind", None)

    # Create new task (validation happens inside create_task)
    task = create_task(
        title=args.title,
        description=args.description,
        priority=priority,
        tags=tags,
        dueDate=dueDate,
        recurrence=recurrence,
        reminderTime=reminderTime,
    )

    # Load existing tasks
    tasks = storage.load_tasks()

    # Add new task to list
    tasks.append(task)

    # Save all tasks
    storage.save_tasks(tasks)

    # Print success message
    print(format_task_created(task))
