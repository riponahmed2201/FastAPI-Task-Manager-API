"""Unit tests for TaskService"""

import pytest
from sqlalchemy.orm import Session
from app import models, schemas
from app.services import UserService, TaskService


class TestTaskService:
    """Tests for TaskService"""
    
    @pytest.fixture
    def user(self, db: Session) -> models.User:
        """Create test user"""
        return UserService.register_user(
            db,
            username="testuser",
            password="password123"
        )
    
    def test_create_task_success(self, db: Session, user: models.User):
        """Test successful task creation"""
        task = TaskService.create_task(
            db,
            user_id=user.id,
            title="Test Task",
            description="Test Description"
        )
        
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.owner_id == user.id
        assert task.completed is False
    
    def test_create_task_empty_title(self, db: Session, user: models.User):
        """Test task creation fails with empty title"""
        with pytest.raises(ValueError):
            TaskService.create_task(
                db,
                user_id=user.id,
                title="",
                description="Test"
            )
    
    def test_complete_task(self, db: Session, user: models.User):
        """Test marking task as complete"""
        task = TaskService.create_task(
            db,
            user_id=user.id,
            title="Test Task"
        )
        
        completed_task = TaskService.complete_task(
            db,
            task_id=task.id,
            user_id=user.id
        )
        
        assert completed_task.completed is True
    
    def test_get_task_statistics(self, db: Session, user: models.User):
        """Test getting task statistics"""
        # Create some tasks
        TaskService.create_task(db, user_id=user.id, title="Task 1")
        TaskService.create_task(db, user_id=user.id, title="Task 2")
        
        # Get statistics
        stats = TaskService.get_task_statistics(db, user.id)
        
        assert stats["total_tasks"] == 2
        assert stats["completed_tasks"] == 0
        assert stats["pending_tasks"] == 2
