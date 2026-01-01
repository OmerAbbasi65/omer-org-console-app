"""Search command - Search tasks by keyword"""

import argparse
from src.domain.task_filter import search_tasks
from src.storage.storage_interface import StorageInterface
from src.cli.formatter import format_task_table


def execute(args: argparse.Namespace, storage: StorageInterface) -> None:
    """
    Execute the search command.

    Searches tasks by keyword (case-insensitive partial match in title/description).

    Args:
        args: Parsed command-line arguments (keyword)
        storage: Storage instance for loading tasks
    """
    # Load all tasks
    tasks = storage.load_tasks()

    # Search tasks
    results = search_tasks(tasks, args.keyword)

    # Format and print results
    print(format_task_table(results))
