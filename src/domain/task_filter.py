"""TaskFilter - Composable AND filtering for tasks"""

from typing import List, Optional
from src.domain.task import Task


class TaskFilter:
    """
    Task filtering with composable AND logic.

    All non-None filter criteria are combined with AND logic.
    """

    def __init__(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        tag: Optional[str] = None,
        keyword: Optional[str] = None,
    ):
        """
        Initialize task filter.

        Args:
            status: Filter by completion status ("complete" or "incomplete")
            priority: Filter by priority level ("high", "medium", "low")
            tag: Filter by tag (must be in task's tags list)
            keyword: Filter by keyword (case-insensitive partial match in title/description)
        """
        self.status = status
        self.priority = priority
        self.tag = tag
        self.keyword = keyword

    def matches(self, task: Task) -> bool:
        """
        Check if a task matches all filter criteria.

        Args:
            task: Task to check

        Returns:
            True if task matches all non-None criteria, False otherwise
        """
        # Status filter
        if self.status is not None:
            if self.status == "complete" and not task.completed:
                return False
            if self.status == "incomplete" and task.completed:
                return False

        # Priority filter
        if self.priority is not None:
            if task.priority != self.priority:
                return False

        # Tag filter
        if self.tag is not None:
            if self.tag not in task.tags:
                return False

        # Keyword filter (case-insensitive partial match)
        if self.keyword is not None:
            keyword_lower = self.keyword.lower()
            title_match = keyword_lower in task.title.lower()
            description_match = (
                task.description is not None and keyword_lower in task.description.lower()
            )
            if not (title_match or description_match):
                return False

        # All criteria matched
        return True

    def apply(self, tasks: List[Task]) -> List[Task]:
        """
        Apply filter to a list of tasks.

        Args:
            tasks: List of tasks to filter

        Returns:
            Filtered list of tasks matching all criteria
        """
        return [task for task in tasks if self.matches(task)]


def search_tasks(tasks: List[Task], keyword: str) -> List[Task]:
    """
    Search tasks by keyword (case-insensitive partial match).

    Searches in both title and description fields.

    Args:
        tasks: List of tasks to search
        keyword: Search keyword

    Returns:
        List of tasks containing the keyword
    """
    filter_obj = TaskFilter(keyword=keyword)
    return filter_obj.apply(tasks)
