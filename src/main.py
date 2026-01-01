"""Main entry point for the todo CLI application"""

import sys
from src.cli.parser import parse_args
from src.cli.formatter import format_error
from src.storage.file_storage import FileStorage
from src.storage.storage_interface import StorageError
from src.domain.validation import ValidationError


def main() -> None:
    """
    Main entry point for the todo application.

    Parses arguments, initializes storage, and dispatches to command handlers.
    """
    try:
        # Parse command-line arguments
        args = parse_args()

        # Initialize storage
        storage = FileStorage()
        storage.ensure_storage_exists()

        # Dispatch to command handler based on parsed command
        # Command handlers will be implemented in Phase 3 (User Story 1)
        command = args.command

        if command == "add":
            from src.cli.commands.level1 import add

            add.execute(args, storage)

        elif command == "list":
            from src.cli.commands.level1 import list_tasks

            list_tasks.execute(args, storage)

        elif command == "update":
            from src.cli.commands.level1 import update

            update.execute(args, storage)

        elif command == "complete":
            from src.cli.commands.level1 import complete

            complete.execute(args, storage)

        elif command == "incomplete":
            from src.cli.commands.level1 import incomplete

            incomplete.execute(args, storage)

        elif command == "delete":
            from src.cli.commands.level1 import delete

            delete.execute(args, storage)

        # Level 2 commands
        elif command == "set-priority":
            from src.cli.commands.level2 import set_priority

            set_priority.execute(args, storage)

        elif command == "set-tags":
            from src.cli.commands.level2 import set_tags

            set_tags.execute(args, storage)

        elif command == "search":
            from src.cli.commands.level2 import search

            search.execute(args, storage)

        elif command == "filter":
            from src.cli.commands.level2 import filter

            filter.execute(args, storage)

        elif command == "sort":
            from src.cli.commands.level2 import sort

            sort.execute(args, storage)

        # Level 3 commands (to be added)
        # elif command == "set-due":
        #     from src.cli.commands.level3 import set_due
        #     set_due.execute(args, storage)
        # ...

        else:
            print(format_error(f"Unknown command: {command}"))
            sys.exit(1)

    except ValidationError as e:
        print(format_error(str(e)))
        sys.exit(1)

    except StorageError as e:
        print(format_error(f"Storage error: {e}"))
        sys.exit(1)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(130)

    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
