"""Filter command - Filter tasks by criteria"""

import argparse
from src.domain.task_filter import TaskFilter
from src.storage.storage_interface import StorageInterface
from src.cli.formatter import format_task_table, format_error


def execute(args: argparse.Namespace, storage: StorageInterface) -> None:
    """
    Execute the filter command.

    Filters tasks by status, priority, and/or tag (composable AND logic).

    Args:
        args: Parsed command-line arguments (status, priority, tag)
        storage: Storage instance for loading tasks
    """
    # Check that at least one filter is provided
    status = getattr(args, "status", None)
    priority = getattr(args, "priority", None)
    tag = getattr(args, "tag", None)

    if status is None and priority is None and tag is None:
        print(format_error("At least one filter (--status, --priority, or --tag) must be provided"))
        return

    # Load all tasks
    tasks = storage.load_tasks()

    # Create and apply filter
    task_filter = TaskFilter(status=status, priority=priority, tag=tag)
    results = task_filter.apply(tasks)

    # Format and print results
    print(format_task_table(results))
