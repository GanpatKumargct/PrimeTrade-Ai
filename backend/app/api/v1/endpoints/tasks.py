from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User, RoleEnum
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services import task_service

router = APIRouter()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Create new task."""
    return task_service.create_user_task(db, task_in=task_in, owner_id=current_user.id)

@router.get("/", response_model=List[TaskResponse])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Retrieve tasks."""
    return task_service.get_tasks(db, user=current_user, skip=skip, limit=limit)

@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get task by ID."""
    task = task_service.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Update a task."""
    task = task_service.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return task_service.update_task(db, db_task=task, task_in=task_in)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> None:
    """Delete a task."""
    task = task_service.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    task_service.delete_task(db, db_task=task)
    return None
