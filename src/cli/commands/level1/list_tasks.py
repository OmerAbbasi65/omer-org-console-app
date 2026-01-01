"""List command - Display all tasks"""

import argparse
from src.storage.storage_interface import StorageInterface
from src.cli.formatter import format_task_table


def execute(args: argparse.Namespace, storage: StorageInterface) -> None:
    """
    Execute the list command.

    Loads all tasks from storage and displays them in a tabular format.

    Args:
        args: Parsed command-line arguments (none for basic list)
        storage: Storage instance for loading tasks
    """
    # Load all tasks
    tasks = storage.load_tasks()

    # Format and print table
    print(format_task_table(tasks))
