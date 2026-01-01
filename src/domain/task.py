"""Task entity - Core business object representing a todo item"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import time


@dataclass
class Task:
    """
    Task entity representing a todo item.

    Level 1 (Basic) fields included in this initial implementation:
    - id: Unique identifier (format: task-<unix-timestamp-ms>)
    - title: Task title (required, max 500 chars)
    - description: Extended description (optional, max 5000 chars)
    - completed: Completion status (boolean, defaults to False)
    - createdAt: Creation timestamp (ISO-8601, immutable)
    - updatedAt: Last modification timestamp (ISO-8601)

    Future levels will extend this with:
    - Level 2: priority, tags
    - Level 3: dueDate, recurrence, reminderTime, lastNotified
    """

    # Level 1 - Basic fields
    id: str
    title: str
    description: Optional[str]
    completed: bool
    createdAt: str
    updatedAt: str

    # Level 2 - Intermediate fields
    priority: Optional[str] = None
    tags: list[str] = field(default_factory=list)

    # Level 3 - Advanced fields
    dueDate: Optional[str] = None
    recurrence: str = "none"
    reminderTime: Optional[str] = None
    lastNotified: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Convert Task to dictionary representation for JSON serialization.

        Returns:
            Dictionary with all task fields
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority,
            "tags": self.tags,
            "dueDate": self.dueDate,
            "recurrence": self.recurrence,
            "reminderTime": self.reminderTime,
            "lastNotified": self.lastNotified,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        """
        Create Task instance from dictionary (deserialization).

        Args:
            data: Dictionary containing task fields

        Returns:
            Task instance

        Raises:
            ValueError: If required fields are missing or invalid
        """
        # Validate required fields exist
        required_fields = ["id", "title", "completed", "createdAt", "updatedAt"]
        for field_name in required_fields:
            if field_name not in data:
                raise ValueError(f"Missing required field: {field_name}")

        return Task(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            completed=data["completed"],
            priority=data.get("priority"),
            tags=data.get("tags", []),
            dueDate=data.get("dueDate"),
            recurrence=data.get("recurrence", "none"),
            reminderTime=data.get("reminderTime"),
            lastNotified=data.get("lastNotified"),
            createdAt=data["createdAt"],
            updatedAt=data["updatedAt"],
        )


def generate_task_id() -> str:
    """
    Generate unique task ID based on current timestamp.

    Format: task-<unix-timestamp-ms>
    Example: task-1735707600000

    Returns:
        Unique task ID string
    """
    timestamp_ms = int(time.time() * 1000)
    return f"task-{timestamp_ms}"


def get_current_timestamp() -> str:
    """
    Get current timestamp in ISO-8601 format.

    Returns:
        Current timestamp as ISO-8601 string (e.g., "2026-01-01T12:00:00Z")
    """
    return datetime.utcnow().isoformat() + "Z"


def is_overdue(task: Task) -> bool:
    """
    Check if a task is overdue.

    A task is overdue if:
    - It has a dueDate set
    - The dueDate is in the past
    - The task is not completed

    Args:
        task: Task to check

    Returns:
        True if task is overdue, False otherwise
    """
    if task.dueDate is None or task.completed:
        return False

    try:
        due = datetime.fromisoformat(task.dueDate.replace("Z", "+00:00"))
        now = datetime.utcnow()
        return due < now
    except (ValueError, AttributeError):
        return False


def create_task(
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[list[str]] = None,
    dueDate: Optional[str] = None,
    recurrence: str = "none",
    reminderTime: Optional[str] = None,
) -> Task:
    """
    Create a new Task with auto-generated ID and timestamps.

    Args:
        title: Task title (required)
        description: Optional extended description
        priority: Optional priority level (high, medium, low)
        tags: Optional list of tags
        dueDate: Optional due date (ISO-8601)
        recurrence: Recurrence pattern (none, daily, weekly, monthly)
        reminderTime: Optional reminder time (ISO-8601)

    Returns:
        New Task instance with generated ID and timestamps

    Raises:
        ValidationError: If validation fails
    """
    from src.domain.validation import validate_task_creation

    # Validate inputs
    validate_task_creation(title, description, priority, tags, dueDate, recurrence, reminderTime)

    now = get_current_timestamp()
    task_id = generate_task_id()

    return Task(
        id=task_id,
        title=title,
        description=description,
        completed=False,
        priority=priority,
        tags=tags if tags is not None else [],
        dueDate=dueDate,
        recurrence=recurrence,
        reminderTime=reminderTime,
        lastNotified=None,
        createdAt=now,
        updatedAt=now,
    )
