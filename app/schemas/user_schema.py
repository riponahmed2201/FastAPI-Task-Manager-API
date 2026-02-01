"""User schemas for request/response validation"""

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """User creation/registration schema"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)


class User(BaseModel):
    """User response schema"""
    id: int
    username: str
    
    class Config:
        from_attributes = True
