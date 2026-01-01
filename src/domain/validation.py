"""Task validation logic"""

from typing import Optional


class ValidationError(Exception):
    """Raised when task validation fails"""

    pass


# Valid priority levels
VALID_PRIORITIES = ["high", "medium", "low"]

# Valid recurrence patterns
VALID_RECURRENCE = ["none", "daily", "weekly", "monthly"]


def validate_title(title: str) -> None:
    """
    Validate task title.

    Rules:
    - Must be non-empty (after stripping whitespace)
    - Maximum 500 characters

    Args:
        title: The title to validate

    Raises:
        ValidationError: If validation fails
    """
    if not title or not title.strip():
        raise ValidationError("Task title cannot be empty")

    if len(title) > 500:
        raise ValidationError(f"Task title too long: {len(title)} chars (max 500)")


def validate_description(description: Optional[str]) -> None:
    """
    Validate task description.

    Rules:
    - Optional (can be None)
    - Maximum 5000 characters if provided

    Args:
        description: The description to validate (can be None)

    Raises:
        ValidationError: If validation fails
    """
    if description is not None and len(description) > 5000:
        raise ValidationError(
            f"Task description too long: {len(description)} chars (max 5000)"
        )


def validate_priority(priority: Optional[str]) -> None:
    """
    Validate task priority.

    Rules:
    - Optional (can be None)
    - Must be one of: high, medium, low

    Args:
        priority: The priority to validate (can be None)

    Raises:
        ValidationError: If validation fails
    """
    if priority is not None and priority not in VALID_PRIORITIES:
        raise ValidationError(
            f"Invalid priority: {priority}. Must be one of: {', '.join(VALID_PRIORITIES)}"
        )


def validate_tags(tags: Optional[list[str]]) -> None:
    """
    Validate task tags.

    Rules:
    - Optional (can be None or empty list)
    - Each tag maximum 50 characters

    Args:
        tags: The tags list to validate (can be None)

    Raises:
        ValidationError: If validation fails
    """
    if tags is not None:
        for tag in tags:
            if len(tag) > 50:
                raise ValidationError(f"Tag too long: '{tag}' ({len(tag)} chars, max 50)")


def validate_iso8601(date_str: Optional[str], field_name: str) -> None:
    """
    Validate ISO-8601 datetime format.

    Args:
        date_str: Date string to validate (can be None)
        field_name: Name of field for error messages

    Raises:
        ValidationError: If validation fails
    """
    if date_str is None:
        return

    from datetime import datetime

    try:
        datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        raise ValidationError(f"Invalid {field_name} format. Must be ISO-8601 (e.g., 2026-01-15T14:00:00Z)")


def validate_recurrence(recurrence: str) -> None:
    """
    Validate recurrence pattern.

    Args:
        recurrence: Recurrence pattern

    Raises:
        ValidationError: If validation fails
    """
    if recurrence not in VALID_RECURRENCE:
        raise ValidationError(
            f"Invalid recurrence: {recurrence}. Must be one of: {', '.join(VALID_RECURRENCE)}"
        )


def validate_reminder(reminderTime: Optional[str], dueDate: Optional[str]) -> None:
    """
    Validate reminder time is before due date.

    Args:
        reminderTime: Reminder time (can be None)
        dueDate: Due date (can be None)

    Raises:
        ValidationError: If validation fails
    """
    if reminderTime is None:
        return

    if dueDate is None:
        raise ValidationError("Reminder time requires a due date to be set")

    from datetime import datetime

    try:
        reminder = datetime.fromisoformat(reminderTime.replace("Z", "+00:00"))
        due = datetime.fromisoformat(dueDate.replace("Z", "+00:00"))

        if reminder >= due:
            raise ValidationError("Reminder time must be before due date")
    except (ValueError, AttributeError):
        raise ValidationError("Invalid datetime format for reminder or due date")


def validate_task_creation(
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[list[str]] = None,
    dueDate: Optional[str] = None,
    recurrence: str = "none",
    reminderTime: Optional[str] = None,
) -> None:
    """
    Validate all fields for task creation.

    Args:
        title: Task title
        description: Optional description
        priority: Optional priority level
        tags: Optional tags list
        dueDate: Optional due date (ISO-8601)
        recurrence: Recurrence pattern
        reminderTime: Optional reminder time (ISO-8601)

    Raises:
        ValidationError: If any validation fails
    """
    validate_title(title)
    validate_description(description)
    validate_priority(priority)
    validate_tags(tags)
    validate_iso8601(dueDate, "due date")
    validate_recurrence(recurrence)
    validate_iso8601(reminderTime, "reminder time")
    validate_reminder(reminderTime, dueDate)

    # Additional constraint: recurrence requires dueDate
    if recurrence != "none" and dueDate is None:
        raise ValidationError("Recurrence pattern requires a due date to be set")


def validate_task_update(
    title: Optional[str] = None, description: Optional[str] = None
) -> None:
    """
    Validate fields for task update.

    Args:
        title: New title (if being updated)
        description: New description (if being updated)

    Raises:
        ValidationError: If any validation fails
    """
    if title is not None:
        validate_title(title)
    if description is not None:
        validate_description(description)
