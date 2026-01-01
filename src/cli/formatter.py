"""Output formatting for CLI display"""

from typing import List
from src.domain.task import Task


def format_task_table(tasks: List[Task]) -> str:
    """
    Format tasks as a tabular display.

    Output format (includes Level 2 fields):
    +------------------+----------+----------+--------+-------+-----------+
    | ID               | Title    | Priority | Tags   | Status|           |
    +------------------+----------+----------+--------+-------+-----------+

    Args:
        tasks: List of Task objects to display

    Returns:
        Formatted table string
    """
    if not tasks:
        return "No tasks found."

    # Column widths
    id_width = 20
    title_width = 25
    priority_width = 8
    tags_width = 15
    status_width = 10

    # Helper to truncate text
    def truncate(text: str | None, width: int) -> str:
        if text is None:
            return "-"
        if len(text) <= width:
            return text
        return text[: width - 2] + ".."

    # Build table header
    separator = (
        f"+{'-' * (id_width + 2)}+{'-' * (title_width + 2)}+"
        f"{'-' * (priority_width + 2)}+{'-' * (tags_width + 2)}+"
        f"{'-' * (status_width + 2)}+"
    )

    header = (
        f"| {'ID'.ljust(id_width)} | {'Title'.ljust(title_width)} | "
        f"{'Priority'.ljust(priority_width)} | {'Tags'.ljust(tags_width)} | "
        f"{'Status'.ljust(status_width)} |"
    )

    lines = [separator, header, separator]

    # Build table rows
    for task in tasks:
        status = "Complete" if task.completed else "Incomplete"
        priority = task.priority if task.priority else "-"
        tags_str = ", ".join(task.tags) if task.tags else "-"

        row = (
            f"| {truncate(task.id, id_width).ljust(id_width)} | "
            f"{truncate(task.title, title_width).ljust(title_width)} | "
            f"{truncate(priority, priority_width).ljust(priority_width)} | "
            f"{truncate(tags_str, tags_width).ljust(tags_width)} | "
            f"{status.ljust(status_width)} |"
        )
        lines.append(row)

    lines.append(separator)

    return "\n".join(lines)


def format_success(message: str) -> str:
    """
    Format success message.

    Args:
        message: Success message text

    Returns:
        Formatted success message
    """
    return f"[OK] {message}"


def format_error(message: str) -> str:
    """
    Format error message.

    Args:
        message: Error message text

    Returns:
        Formatted error message
    """
    return f"[ERROR] {message}"


def format_task_created(task: Task) -> str:
    """
    Format message for successful task creation.

    Args:
        task: The created task

    Returns:
        Formatted success message
    """
    return format_success(f"Task created with ID: {task.id}")


def format_task_updated(task_id: str) -> str:
    """
    Format message for successful task update.

    Args:
        task_id: ID of updated task

    Returns:
        Formatted success message
    """
    return format_success(f"Task {task_id} updated successfully")


def format_task_completed(task_id: str) -> str:
    """
    Format message for successful task completion.

    Args:
        task_id: ID of completed task

    Returns:
        Formatted success message
    """
    return format_success(f"Task {task_id} marked as complete")


def format_task_incompleted(task_id: str) -> str:
    """
    Format message for marking task incomplete.

    Args:
        task_id: ID of task marked incomplete

    Returns:
        Formatted success message
    """
    return format_success(f"Task {task_id} marked as incomplete")


def format_task_deleted(task_id: str) -> str:
    """
    Format message for successful task deletion.

    Args:
        task_id: ID of deleted task

    Returns:
        Formatted success message
    """
    return format_success(f"Task {task_id} deleted successfully")


def format_task_not_found(task_id: str) -> str:
    """
    Format error message for task not found.

    Args:
        task_id: ID of task that wasn't found

    Returns:
        Formatted error message
    """
    return format_error(f"Task with ID '{task_id}' not found")
