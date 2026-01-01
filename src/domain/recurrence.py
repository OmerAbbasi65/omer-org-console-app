"""Recurrence calculation functions"""

from datetime import datetime, timedelta
from typing import Optional
import calendar


def calculate_next_due_date(current_due_date: str, recurrence: str) -> Optional[str]:
    """
    Calculate the next due date based on recurrence pattern.

    Args:
        current_due_date: Current due date in ISO-8601 format
        recurrence: Recurrence pattern ("none", "daily", "weekly", "monthly")

    Returns:
        Next due date in ISO-8601 format, or None if recurrence is "none"

    Raises:
        ValueError: If date format is invalid or recurrence pattern is unknown
    """
    if recurrence == "none":
        return None

    try:
        # Parse ISO-8601 datetime
        current = datetime.fromisoformat(current_due_date.replace("Z", "+00:00"))

        # Calculate next date based on recurrence pattern
        if recurrence == "daily":
            next_date = current + timedelta(days=1)
        elif recurrence == "weekly":
            next_date = current + timedelta(weeks=1)
        elif recurrence == "monthly":
            # Handle month-end edge cases (e.g., Jan 31 -> Feb 28/29)
            # Add one month, handling day overflow
            year = current.year
            month = current.month + 1
            if month > 12:
                month = 1
                year += 1

            # Get last day of target month
            last_day = calendar.monthrange(year, month)[1]
            day = min(current.day, last_day)

            next_date = current.replace(year=year, month=month, day=day)
        else:
            raise ValueError(f"Unknown recurrence pattern: {recurrence}")

        # Return as ISO-8601 string
        return next_date.isoformat().replace("+00:00", "Z")

    except (ValueError, AttributeError) as e:
        raise ValueError(f"Invalid date format or recurrence: {e}") from e
