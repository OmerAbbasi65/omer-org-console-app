"""TaskSort - Multi-field sorting for tasks"""

from typing import List
from src.domain.task import Task


class TaskSort:
    """Task sorting by multiple fields with ascending/descending order."""

    # Priority ordering (high > medium > low > null)
    PRIORITY_ORDER = {"high": 3, "medium": 2, "low": 1, None: 0}

    def __init__(self, field: str, direction: str = "asc"):
        """
        Initialize task sorter.

        Args:
            field: Field to sort by (priority, title, dueDate, createdAt)
            direction: Sort direction ("asc" or "desc")
        """
        self.field = field
        self.direction = direction

    def sort(self, tasks: List[Task]) -> List[Task]:
        """
        Sort tasks by the specified field and direction.

        Note: Returns a NEW sorted list. Does not modify the original list.

        Args:
            tasks: List of tasks to sort

        Returns:
            New sorted list of tasks
        """
        # Create a copy to avoid modifying original
        sorted_tasks = tasks.copy()

        # Define sort key based on field
        if self.field == "priority":
            key_func = lambda t: self.PRIORITY_ORDER.get(t.priority, 0)
        elif self.field == "title":
            key_func = lambda t: t.title.lower()
        elif self.field == "dueDate":
            # Sort by dueDate (null values last)
            # key_func = lambda t: (t.dueDate is None, t.dueDate or "")
            # For Level 2, dueDate doesn't exist yet, so use createdAt as fallback
            key_func = lambda t: t.createdAt
        elif self.field == "createdAt":
            key_func = lambda t: t.createdAt
        else:
            # Default to createdAt if unknown field
            key_func = lambda t: t.createdAt

        # Sort with appropriate direction
        reverse = self.direction == "desc"
        sorted_tasks.sort(key=key_func, reverse=reverse)

        return sorted_tasks


def sort_tasks(tasks: List[Task], field: str, direction: str = "asc") -> List[Task]:
    """
    Sort tasks by field and direction.

    Args:
        tasks: List of tasks to sort
        field: Field to sort by (priority, title, dueDate, createdAt)
        direction: Sort direction ("asc" or "desc")

    Returns:
        New sorted list of tasks (original list unchanged)
    """
    sorter = TaskSort(field, direction)
    return sorter.sort(tasks)
