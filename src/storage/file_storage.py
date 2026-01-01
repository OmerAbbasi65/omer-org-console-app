"""File-based storage implementation using JSON"""

import json
import os
from pathlib import Path
from typing import List
from src.domain.task import Task
from src.storage.storage_interface import StorageInterface, StorageError


class FileStorage(StorageInterface):
    """
    File-based storage implementation.

    Stores tasks as JSON array in user's home directory at ~/.todo-data.json
    Uses atomic writes (temp file + rename) to prevent data corruption.
    """

    def __init__(self, file_path: str | None = None) -> None:
        """
        Initialize FileStorage.

        Args:
            file_path: Optional custom file path (defaults to ~/.todo-data.json)
        """
        if file_path is None:
            # Default to ~/.todo-data.json in user's home directory
            home = Path.home()
            self.file_path = home / ".todo-data.json"
        else:
            self.file_path = Path(file_path)

        self.temp_file_path = Path(str(self.file_path) + ".tmp")

    def ensure_storage_exists(self) -> None:
        """
        Ensure storage file exists.

        Creates an empty JSON array file if it doesn't exist.
        Idempotent - safe to call multiple times.

        Raises:
            StorageError: If file cannot be created
        """
        try:
            if not self.file_path.exists():
                # Create empty JSON array
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=2)
        except (OSError, IOError) as e:
            raise StorageError(f"Failed to create storage file: {e}") from e

    def load_tasks(self) -> List[Task]:
        """
        Load all tasks from JSON file.

        Returns:
            List of Task objects (empty list if file doesn't exist or is corrupted)

        Implements graceful degradation:
        - Missing file → returns empty list
        - Corrupted JSON → returns empty list (logs error internally)
        """
        # If file doesn't exist, return empty list
        if not self.file_path.exists():
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Validate root is an array
            if not isinstance(data, list):
                raise StorageError("Invalid storage format: root must be array")

            # Deserialize each task
            tasks = []
            for item in data:
                try:
                    task = Task.from_dict(item)
                    tasks.append(task)
                except (ValueError, KeyError) as e:
                    # Log error but continue loading other tasks
                    # In production, would use proper logging
                    print(f"Warning: Skipping invalid task: {e}")
                    continue

            return tasks

        except json.JSONDecodeError as e:
            # Corrupted JSON - graceful degradation to empty list
            print(f"Warning: Corrupted storage file, starting fresh: {e}")
            return []
        except (OSError, IOError) as e:
            raise StorageError(f"Failed to read storage file: {e}") from e

    def save_tasks(self, tasks: List[Task]) -> None:
        """
        Save all tasks to JSON file using atomic write.

        Atomic write process:
        1. Write to temporary file (.todo-data.json.tmp)
        2. Rename temp file to actual file (atomic on POSIX, near-atomic on Windows)

        Args:
            tasks: List of Task objects to persist

        Raises:
            StorageError: If saving fails
        """
        try:
            # Serialize tasks to dictionaries
            task_dicts = [task.to_dict() for task in tasks]

            # Write to temporary file
            with open(self.temp_file_path, "w", encoding="utf-8") as f:
                json.dump(task_dicts, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())  # Ensure data is written to disk

            # Atomic rename (replaces existing file)
            self.temp_file_path.replace(self.file_path)

        except (OSError, IOError, json.JSONEncodeError) as e:
            # Clean up temp file if it exists
            if self.temp_file_path.exists():
                try:
                    self.temp_file_path.unlink()
                except OSError:
                    pass  # Best effort cleanup

            raise StorageError(f"Failed to save tasks: {e}") from e
