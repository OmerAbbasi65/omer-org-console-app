"""Storage interface - Abstract base for task persistence"""

from abc import ABC, abstractmethod
from typing import List
from src.domain.task import Task


class StorageInterface(ABC):
    """
    Abstract interface for task storage.

    Defines the minimal contract for persisting and retrieving tasks.
    Implementations must provide concrete persistence mechanisms (file, database, etc).
    """

    @abstractmethod
    def load_tasks(self) -> List[Task]:
        """
        Load all tasks from storage.

        Returns:
            List of Task objects (empty list if no tasks exist)

        Raises:
            StorageError: If loading fails critically
        """
        pass

    @abstractmethod
    def save_tasks(self, tasks: List[Task]) -> None:
        """
        Save all tasks to storage.

        This operation should be atomic - either all tasks are saved
        successfully or none are modified.

        Args:
            tasks: List of Task objects to persist

        Raises:
            StorageError: If saving fails
        """
        pass

    @abstractmethod
    def ensure_storage_exists(self) -> None:
        """
        Ensure storage location exists and is accessible.

        Creates storage if it doesn't exist (e.g., creates file or database).
        Should be idempotent - safe to call multiple times.

        Raises:
            StorageError: If storage cannot be created or accessed
        """
        pass


class StorageError(Exception):
    """Raised when storage operations fail"""

    pass
