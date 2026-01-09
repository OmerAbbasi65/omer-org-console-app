"""Task API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
from uuid import UUID

from src.database import get_session
from src.models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from src.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
):
    """Create a new task."""
    created_task = TaskService.create_task(session, task)
    return created_task


@router.get("", response_model=dict)
def list_tasks(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    """List tasks with pagination."""
    tasks, total = TaskService.get_tasks(session, status, limit, offset)
    return {
        "tasks": tasks,
        "pagination": {
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total,
        },
    }


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    session: Session = Depends(get_session),
):
    """Get a single task by ID."""
    task = TaskService.get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
):
    """Update a task (partial update)."""
    task = TaskService.update_task(session, task_id, task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    session: Session = Depends(get_session),
):
    """Delete a task."""
    deleted = TaskService.delete_task(session, task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return None
