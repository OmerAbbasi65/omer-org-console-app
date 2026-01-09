"""
Task API Endpoints - Level 1 (Core Features)

As defined in: specs/002-todo-web-app-level1/contracts/api-endpoints.md
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from datetime import datetime

from app.db import get_session
from app.models import Task, TaskCreate, TaskUpdate, TaskResponse, TaskList


router = APIRouter()


# Response wrapper helper
def success_response(data):
    """Wrap data in success response format"""
    return {"success": True, "data": data}


def error_response(code: str, message: str, details: dict = None):
    """Create error response format"""
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details or {}
        }
    }


@router.post("/tasks", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new task.

    - **title**: Task title (required, 1-200 characters)
    - **description**: Optional task description (max 1000 characters)

    Returns the created task with auto-generated ID and timestamps.
    """
    try:
        # Create task instance
        task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Add to database
        session.add(task)
        session.commit()
        session.refresh(task)

        # Return success response
        return success_response(TaskResponse.from_orm(task).dict())

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response("VALIDATION_ERROR", str(e))
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("DATABASE_ERROR", "Failed to create task")
        )


@router.get("/tasks", response_model=dict)
def get_all_tasks(session: Session = Depends(get_session)):
    """
    Get all tasks.

    Returns a list of all tasks with their details.
    """
    try:
        statement = select(Task).order_by(Task.created_at.desc())
        tasks = session.exec(statement).all()

        return success_response({
            "tasks": [TaskResponse.from_orm(task).dict() for task in tasks],
            "total": len(tasks)
        })

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("DATABASE_ERROR", "Failed to fetch tasks")
        )


@router.get("/tasks/{task_id}", response_model=dict)
def get_task(
    task_id: UUID,
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.

    - **task_id**: UUID of the task

    Returns the task if found, 404 if not found.
    """
    try:
        task = session.get(Task, task_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response(
                    "TASK_NOT_FOUND",
                    f"Task with ID {task_id} not found",
                    {"taskId": str(task_id)}
                )
            )

        return success_response(TaskResponse.from_orm(task).dict())

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("DATABASE_ERROR", "Failed to fetch task")
        )


@router.patch("/tasks/{task_id}", response_model=dict)
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    session: Session = Depends(get_session)
):
    """
    Update a task's title and/or description.

    - **task_id**: UUID of the task
    - **title**: Updated title (optional)
    - **description**: Updated description (optional)

    At least one field must be provided. Returns updated task.
    """
    try:
        # Find task
        task = session.get(Task, task_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response(
                    "TASK_NOT_FOUND",
                    f"Task with ID {task_id} not found"
                )
            )

        # Check if at least one field is provided
        if task_data.title is None and task_data.description is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_response(
                    "VALIDATION_ERROR",
                    "At least one field (title or description) must be provided for update"
                )
            )

        # Update fields
        if task_data.title is not None:
            task.title = task_data.title

        if task_data.description is not None:
            task.description = task_data.description

        # Update timestamp
        task.updated_at = datetime.utcnow()

        # Commit changes
        session.add(task)
        session.commit()
        session.refresh(task)

        return success_response(TaskResponse.from_orm(task).dict())

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error_response("VALIDATION_ERROR", str(e))
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("DATABASE_ERROR", "Failed to update task")
        )


@router.patch("/tasks/{task_id}/toggle", response_model=dict)
def toggle_task_completion(
    task_id: UUID,
    session: Session = Depends(get_session)
):
    """
    Toggle a task's completion status.

    - **task_id**: UUID of the task

    Toggles completed from true to false or false to true.
    Returns updated task.
    """
    try:
        # Find task
        task = session.get(Task, task_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response(
                    "TASK_NOT_FOUND",
                    f"Task with ID {task_id} not found"
                )
            )

        # Toggle completion status
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()

        # Commit changes
        session.add(task)
        session.commit()
        session.refresh(task)

        return success_response(TaskResponse.from_orm(task).dict())

    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("DATABASE_ERROR", "Failed to toggle task completion")
        )


@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(
    task_id: UUID,
    session: Session = Depends(get_session)
):
    """
    Delete a task permanently.

    - **task_id**: UUID of the task

    This operation cannot be undone. Returns deletion confirmation.
    """
    try:
        # Find task
        task = session.get(Task, task_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response(
                    "TASK_NOT_FOUND",
                    f"Task with ID {task_id} not found"
                )
            )

        # Delete task
        session.delete(task)
        session.commit()

        return success_response({
            "id": str(task_id),
            "deleted": True
        })

    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("DATABASE_ERROR", "Failed to delete task")
        )
