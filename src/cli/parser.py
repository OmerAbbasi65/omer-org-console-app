"""CLI argument parser and command router"""

import argparse
import sys
from typing import Any


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the main argument parser.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog="todo",
        description="AI-Native Todo Console Application",
        epilog="For help with a specific command, use: todo <command> --help",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Level 1 - Basic Commands
    _add_add_parser(subparsers)
    _add_list_parser(subparsers)
    _add_update_parser(subparsers)
    _add_complete_parser(subparsers)
    _add_incomplete_parser(subparsers)
    _add_delete_parser(subparsers)

    # Level 2 - Intermediate Commands
    _add_set_priority_parser(subparsers)
    _add_set_tags_parser(subparsers)
    _add_search_parser(subparsers)
    _add_filter_parser(subparsers)
    _add_sort_parser(subparsers)

    # Level 3 - Advanced Commands (to be added)
    # _add_set_due_parser(subparsers)
    # _add_set_recurrence_parser(subparsers)
    # _add_set_reminder_parser(subparsers)

    return parser


def _add_add_parser(subparsers: Any) -> None:
    """Add 'add' command parser"""
    parser = subparsers.add_parser("add", help="Add a new task")
    parser.add_argument("title", type=str, help="Task title (required)")
    parser.add_argument(
        "--description", "-d", type=str, default=None, help="Task description (optional)"
    )
    # Level 2 arguments
    parser.add_argument(
        "--priority", "-p", choices=["high", "medium", "low"], default=None, help="Priority"
    )
    parser.add_argument("--tags", "-t", type=str, default=None, help="Comma-separated tags")
    # Level 3 arguments
    parser.add_argument("--due", type=str, default=None, help="Due date (ISO-8601)")
    parser.add_argument(
        "--recurrence",
        "-r",
        choices=["none", "daily", "weekly", "monthly"],
        default="none",
        help="Recurrence pattern",
    )
    parser.add_argument("--remind", type=str, default=None, help="Reminder time (ISO-8601)")


def _add_list_parser(subparsers: Any) -> None:
    """Add 'list' command parser"""
    parser = subparsers.add_parser("list", help="List all tasks")


def _add_update_parser(subparsers: Any) -> None:
    """Add 'update' command parser"""
    parser = subparsers.add_parser("update", help="Update an existing task")
    parser.add_argument("task_id", type=str, help="Task ID to update")
    parser.add_argument("--title", "-t", type=str, default=None, help="New title")
    parser.add_argument(
        "--description", "-d", type=str, default=None, help="New description"
    )


def _add_complete_parser(subparsers: Any) -> None:
    """Add 'complete' command parser"""
    parser = subparsers.add_parser("complete", help="Mark a task as complete")
    parser.add_argument("task_id", type=str, help="Task ID to mark complete")


def _add_incomplete_parser(subparsers: Any) -> None:
    """Add 'incomplete' command parser"""
    parser = subparsers.add_parser("incomplete", help="Mark a task as incomplete")
    parser.add_argument("task_id", type=str, help="Task ID to mark incomplete")


def _add_delete_parser(subparsers: Any) -> None:
    """Add 'delete' command parser"""
    parser = subparsers.add_parser("delete", help="Delete a task")
    parser.add_argument("task_id", type=str, help="Task ID to delete")


def _add_set_priority_parser(subparsers: Any) -> None:
    """Add 'set-priority' command parser"""
    parser = subparsers.add_parser("set-priority", help="Set task priority")
    parser.add_argument("task_id", type=str, help="Task ID")
    parser.add_argument(
        "priority", type=str, choices=["high", "medium", "low"], help="Priority level"
    )


def _add_set_tags_parser(subparsers: Any) -> None:
    """Add 'set-tags' command parser"""
    parser = subparsers.add_parser("set-tags", help="Set task tags")
    parser.add_argument("task_id", type=str, help="Task ID")
    parser.add_argument("tags", type=str, help="Comma-separated tags")


def _add_search_parser(subparsers: Any) -> None:
    """Add 'search' command parser"""
    parser = subparsers.add_parser("search", help="Search tasks by keyword")
    parser.add_argument("keyword", type=str, help="Search keyword")


def _add_filter_parser(subparsers: Any) -> None:
    """Add 'filter' command parser"""
    parser = subparsers.add_parser("filter", help="Filter tasks by criteria")
    parser.add_argument(
        "--status", type=str, choices=["complete", "incomplete"], help="Filter by status"
    )
    parser.add_argument(
        "--priority", type=str, choices=["high", "medium", "low"], help="Filter by priority"
    )
    parser.add_argument("--tag", type=str, help="Filter by tag")


def _add_sort_parser(subparsers: Any) -> None:
    """Add 'sort' command parser"""
    parser = subparsers.add_parser("sort", help="Sort tasks (display only)")
    parser.add_argument(
        "--by",
        type=str,
        required=True,
        choices=["priority", "title", "createdAt"],
        help="Field to sort by",
    )
    parser.add_argument(
        "--order", type=str, default="asc", choices=["asc", "desc"], help="Sort order"
    )


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        args: Optional argument list (defaults to sys.argv[1:])

    Returns:
        Parsed arguments namespace
    """
    parser = create_parser()
    parsed = parser.parse_args(args)

    # If no command provided, show help
    if not parsed.command:
        parser.print_help()
        sys.exit(1)

    return parsed
