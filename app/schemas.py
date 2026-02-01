from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str | None = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    completed: bool
    owner_id: int
    class Config: from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    class Config: from_attributes = True