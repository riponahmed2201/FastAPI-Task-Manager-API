"""Unit tests for UserService"""

import pytest
from sqlalchemy.orm import Session
from app import models, schemas
from app.services import UserService


class TestUserService:
    """Tests for UserService"""
    
    def test_register_user_success(self, db: Session):
        """Test successful user registration"""
        user_data = schemas.UserCreate(
            username="testuser",
            password="password123"
        )
        
        user = UserService.register_user(
            db,
            username=user_data.username,
            password=user_data.password
        )
        
        assert user.username == "testuser"
        assert user.hashed_password is not None
    
    def test_register_user_duplicate(self, db: Session):
        """Test registration fails for duplicate username"""
        user_data = schemas.UserCreate(
            username="testuser",
            password="password123"
        )
        
        # Register first user
        UserService.register_user(
            db,
            username=user_data.username,
            password=user_data.password
        )
        
        # Try to register same username
        with pytest.raises(ValueError):
            UserService.register_user(
                db,
                username=user_data.username,
                password=user_data.password
            )
    
    def test_authenticate_user_success(self, db: Session):
        """Test successful authentication"""
        # Register user
        UserService.register_user(
            db,
            username="testuser",
            password="password123"
        )
        
        # Authenticate
        user = UserService.authenticate_user(
            db,
            username="testuser",
            password="password123"
        )
        
        assert user is not None
        assert user.username == "testuser"
    
    def test_authenticate_user_invalid_password(self, db: Session):
        """Test authentication fails with invalid password"""
        # Register user
        UserService.register_user(
            db,
            username="testuser",
            password="password123"
        )
        
        # Try wrong password
        user = UserService.authenticate_user(
            db,
            username="testuser",
            password="wrongpassword"
        )
        
        assert user is None
