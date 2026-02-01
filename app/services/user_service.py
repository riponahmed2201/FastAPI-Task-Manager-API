"""User service for user business logic"""

from typing import Optional, List
from sqlalchemy.orm import Session
from app import models, repositories
from core.security import get_password_hash, verify_password


class UserService:
    """Service for user business logic"""
    
    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[models.User]:
        """Get user by ID"""
        return repositories.UserRepository.get_by_id(db, user_id)
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
        """Get user by username"""
        return repositories.UserRepository.get_by_username(db, username)
    
    @staticmethod
    def get_all_users(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.User]:
        """Get all users"""
        return repositories.UserRepository.get_all(db, skip, limit)
    
    @staticmethod
    def register_user(
        db: Session,
        username: str,
        password: str,
        email: Optional[str] = None
    ) -> models.User:
        """Register new user with validation"""
        # Check if user exists
        existing_user = repositories.UserRepository.get_by_username(db, username)
        if existing_user:
            raise ValueError(f"User with username '{username}' already exists")
        
        # Validate username length
        if len(username) < 3 or len(username) > 50:
            raise ValueError("Username must be between 3 and 50 characters")
        
        # Validate password strength
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        # Create user
        hashed_password = get_password_hash(password)
        user = models.User(
            username=username,
            hashed_password=hashed_password,
            email=email
        )
        return repositories.UserRepository.create(db, user)
    
    @staticmethod
    def authenticate_user(
        db: Session,
        username: str,
        password: str
    ) -> Optional[models.User]:
        """Authenticate user"""
        user = repositories.UserRepository.get_by_username(db, username)
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        **update_data
    ) -> Optional[models.User]:
        """Update user"""
        return repositories.UserRepository.update(db, user_id, **update_data)
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete user"""
        return repositories.UserRepository.delete(db, user_id)
    
    @staticmethod
    def get_user_statistics(db: Session, user_id: int) -> dict:
        """Get user statistics"""
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
