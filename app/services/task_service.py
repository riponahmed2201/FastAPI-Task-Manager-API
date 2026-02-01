"""Task service for task business logic"""

from typing import Optional, List
from sqlalchemy.orm import Session
from app import models, repositories


class TaskService:
    """Service for task business logic"""
    
    @staticmethod
    def get_task(
        db: Session,
        task_id: int,
        user_id: int
    ) -> Optional[models.Task]:
        """Get task by ID for user"""
        return repositories.TaskRepository.get_by_user_and_id(db, task_id, user_id)
    
    @staticmethod
    def get_user_tasks(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        filter_completed: Optional[bool] = None
    ) -> List[models.Task]:
        """Get user tasks with optional filtering"""
        if filter_completed is None:
            # Get all tasks
            return repositories.TaskRepository.get_by_user(db, user_id, skip, limit)
        elif filter_completed:
            # Get completed tasks
            return repositories.TaskRepository.get_completed_tasks(db, user_id)
        else:
            # Get pending tasks
            return repositories.TaskRepository.get_pending_tasks(db, user_id)
    
    @staticmethod
    def create_task(
        db: Session,
        user_id: int,
        title: str,
        description: Optional[str] = None
    ) -> models.Task:
        """Create new task with validation"""
        # Validate title
        if not title or len(title.strip()) == 0:
            raise ValueError("Task title cannot be empty")
        
        if len(title) > 255:
            raise ValueError("Task title must be less than 255 characters")
        
        # Validate description
        if description and len(description) > 2000:
            raise ValueError("Task description must be less than 2000 characters")
        
        # Create task
        task = models.Task(
            title=title.strip(),
            description=description.strip() if description else None,
            owner_id=user_id
        )
        return repositories.TaskRepository.create(db, task)
    
    @staticmethod
    def update_task(
        db: Session,
        task_id: int,
        user_id: int,
        **update_data
    ) -> Optional[models.Task]:
        """Update task with validation"""
        # Check if task belongs to user
        task = repositories.TaskRepository.get_by_user_and_id(db, task_id, user_id)
        if not task:
            return None
        
        # Validate title if provided
        if "title" in update_data:
            title = update_data["title"]
            if not title or len(title.strip()) == 0:
                raise ValueError("Task title cannot be empty")
            if len(title) > 255:
                raise ValueError("Task title must be less than 255 characters")
            update_data["title"] = title.strip()
        
        # Validate description if provided
        if "description" in update_data and update_data["description"]:
            if len(update_data["description"]) > 2000:
                raise ValueError("Task description must be less than 2000 characters")
            update_data["description"] = update_data["description"].strip()
        
        return repositories.TaskRepository.update(db, task_id, **update_data)
    
    @staticmethod
    def complete_task(
        db: Session,
        task_id: int,
        user_id: int
    ) -> Optional[models.Task]:
        """Mark task as complete"""
        task = repositories.TaskRepository.get_by_user_and_id(db, task_id, user_id)
        if not task:
            return None
        
        task.completed = True
        return repositories.TaskRepository.update(db, task_id, completed=True)
    
    @staticmethod
    def incomplete_task(
        db: Session,
        task_id: int,
        user_id: int
    ) -> Optional[models.Task]:
        """Mark task as incomplete"""
        task = repositories.TaskRepository.get_by_user_and_id(db, task_id, user_id)
        if not task:
            return None
        
        task.completed = False
        return repositories.TaskRepository.update(db, task_id, completed=False)
    
    @staticmethod
    def delete_task(
        db: Session,
        task_id: int,
        user_id: int
    ) -> bool:
        """Delete task"""
        # Check if task belongs to user
        task = repositories.TaskRepository.get_by_user_and_id(db, task_id, user_id)
        if not task:
            return False
        
        return repositories.TaskRepository.delete(db, task_id)
    
    @staticmethod
    def get_task_statistics(db: Session, user_id: int) -> dict:
        """Get task statistics for user"""
        total_tasks = repositories.TaskRepository.count_by_user(db, user_id)
        completed_tasks = repositories.TaskRepository.count_completed_by_user(db, user_id)
        pending_tasks = total_tasks - completed_tasks
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "completion_percentage": (
                (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            )
        }
