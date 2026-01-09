"""Task service with business logic."""

from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from src.models.task import Task, TaskCreate, TaskUpdate


class TaskService:
    """Service for task operations."""

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate) -> Task:
        """Create a new task."""
        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority or "medium",
            tags=task_data.tags or [],
            due_date=task_data.due_date,
            recurrence=task_data.recurrence or "none",
            completed=False,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_task_by_id(session: Session, task_id: UUID) -> Optional[Task]:
        """Get a task by ID."""
        return session.get(Task, task_id)

    @staticmethod
    def get_tasks(
        session: Session,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[List[Task], int]:
        """Get tasks with pagination and optional filtering."""
        query = select(Task)

        # Filter by status
        if status == "active":
            query = query.where(Task.completed == False)  # noqa: E712
        elif status == "completed":
            query = query.where(Task.completed == True)  # noqa: E712

        # Count total
        total = len(session.exec(query).all())

        # Apply pagination and ordering
        query = query.order_by(Task.created_at.desc()).offset(offset).limit(limit)
        tasks = session.exec(query).all()

        return list(tasks), total

    @staticmethod
    def update_task(
        session: Session,
        task_id: UUID,
        task_data: TaskUpdate,
    ) -> Optional[Task]:
        """Update a task with partial data."""
        task = session.get(Task, task_id)
        if not task:
            return None

        # Update only provided fields
        update_data = task_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: UUID) -> bool:
        """Delete a task (hard delete)."""
        task = session.get(Task, task_id)
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True
