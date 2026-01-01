"""Sort command - Sort tasks by field (display only)"""

import argparse
from src.domain.task_sort import sort_tasks
from src.storage.storage_interface import StorageInterface
from src.cli.formatter import format_task_table


def execute(args: argparse.Namespace, storage: StorageInterface) -> None:
    """
    Execute the sort command.

    Sorts and displays tasks by the specified field and order.
    Note: This is display-only and does NOT modify storage.

    Args:
        args: Parsed command-line arguments (by, order)
        storage: Storage instance for loading tasks
    """
    # Load all tasks
    tasks = storage.load_tasks()

    # Sort tasks (returns new sorted list, doesn't modify original)
    sorted_tasks = sort_tasks(tasks, field=args.by, direction=args.order)

    # Format and print results (display only, no save)
    print(format_task_table(sorted_tasks))
