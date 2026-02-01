"""Task schemas for request/response validation"""

from pydantic import BaseModel, Field
from typing import Optional


class TaskBase(BaseModel):
    """Base task schema"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)


class TaskCreate(TaskBase):
    """Task creation schema"""
    pass


class TaskUpdate(BaseModel):
    """Task update schema"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    completed: Optional[bool] = None


class Task(TaskBase):
    """Task response schema"""
    id: int
    completed: bool
    owner_id: int
    
    class Config:
        from_attributes = True
