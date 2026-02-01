from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import logging

from app import models, schemas
from app.database import get_db
from app.services import TaskService
from core.security import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=dict)
def read_tasks(
    skip: int = Query(0, ge=0, description="Items to skip"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    completed: bool | None = Query(None, description="Filter by completion status"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all tasks for current user"""
    tasks = TaskService.get_user_tasks(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        filter_completed=completed
    )
    
    total = TaskService.get_task_statistics(db, current_user.id)["total_tasks"]
    
    return {
        "items": tasks,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.post("/", response_model=schemas.Task, status_code=201)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new task"""
    try:
        db_task = TaskService.create_task(
            db,
            user_id=current_user.id,
            title=task.title,
            description=task.description
        )
        logger.info(f"Task created: {db_task.id} by user {current_user.username}")
        return db_task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}", response_model=schemas.Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get task by ID"""
    task = TaskService.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update a task"""
    try:
        update_data = task_update.model_dump(exclude_unset=True)
        task = TaskService.update_task(
            db,
            task_id=task_id,
            user_id=current_user.id,
            **update_data
        )
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        logger.info(f"Task updated: {task_id}")
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{task_id}/complete", response_model=schemas.Task)
def mark_task_complete(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Mark task as complete"""
    task = TaskService.complete_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}/incomplete", response_model=schemas.Task)
def mark_task_incomplete(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Mark task as incomplete"""
    task = TaskService.incomplete_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}")
def remove_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete a task"""
    success = TaskService.delete_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"Task deleted: {task_id}")
    return {"message": "Task deleted successfully"}


@router.get("/statistics/summary")
def get_task_statistics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get task statistics"""
    statistics = TaskService.get_task_statistics(db, current_user.id)
    return statistics