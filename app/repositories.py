"""
Repository pattern for database access layer.
This module handles all database operations in a clean, reusable way.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from . import models, schemas


class UserRepository:
    """Repository for User database operations"""
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[models.User]:
        """Get user by ID"""
        return db.query(models.User).filter(models.User.id == user_id).first()
    
    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[models.User]:
        """Get user by username"""
        return db.query(models.User).filter(
            models.User.username == username
        ).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
        """Get all users with pagination"""
        return db.query(models.User).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, user: models.User) -> models.User:
        """Create new user"""
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update(db: Session, user_id: int, **kwargs) -> Optional[models.User]:
        """Update user"""
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            db.commit()
            db.refresh(user)
        return user
    
    @staticmethod
    def delete(db: Session, user_id: int) -> bool:
        """Delete user"""
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
    
    @staticmethod
    def count(db: Session) -> int:
        """Count total users"""
        return db.query(models.User).count()


class TaskRepository:
    """Repository for Task database operations"""
    
    @staticmethod
    def get_by_id(db: Session, task_id: int) -> Optional[models.Task]:
        """Get task by ID"""
        return db.query(models.Task).filter(models.Task.id == task_id).first()
    
    @staticmethod
    def get_by_user(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Task]:
        """Get all tasks for user"""
        return db.query(models.Task).filter(
            models.Task.owner_id == user_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_user_and_id(
        db: Session,
        task_id: int,
        user_id: int
    ) -> Optional[models.Task]:
        """Get task by ID and user"""
        return db.query(models.Task).filter(
            models.Task.id == task_id,
            models.Task.owner_id == user_id
        ).first()
    
    @staticmethod
    def get_completed_tasks(db: Session, user_id: int) -> List[models.Task]:
        """Get completed tasks for user"""
        return db.query(models.Task).filter(
            models.Task.owner_id == user_id,
            models.Task.completed == True
        ).all()
    
    @staticmethod
    def get_pending_tasks(db: Session, user_id: int) -> List[models.Task]:
        """Get pending tasks for user"""
        return db.query(models.Task).filter(
            models.Task.owner_id == user_id,
            models.Task.completed == False
        ).all()
    
    @staticmethod
    def create(db: Session, task: models.Task) -> models.Task:
        """Create new task"""
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    @staticmethod
    def update(db: Session, task_id: int, **kwargs) -> Optional[models.Task]:
        """Update task"""
        task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key) and value is not None:
                    setattr(task, key, value)
            db.commit()
            db.refresh(task)
        return task
    
    @staticmethod
    def delete(db: Session, task_id: int) -> bool:
        """Delete task"""
        task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if task:
            db.delete(task)
            db.commit()
            return True
        return False
    
    @staticmethod
    def count_by_user(db: Session, user_id: int) -> int:
        """Count tasks for user"""
        return db.query(models.Task).filter(
            models.Task.owner_id == user_id
        ).count()
    
    @staticmethod
    def count_completed_by_user(db: Session, user_id: int) -> int:
        """Count completed tasks for user"""
        return db.query(models.Task).filter(
            models.Task.owner_id == user_id,
            models.Task.completed == True
        ).count()
