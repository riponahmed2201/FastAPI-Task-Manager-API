# Advanced Implementation Guide - Task Manager API

Practical examples for implementing best practices in your Task Manager API.

## 📚 Table of Contents

1. [Enhanced Configuration](#enhanced-configuration)
2. [Improved Database Models](#improved-database-models)
3. [Advanced Schemas with Validation](#advanced-schemas-with-validation)
4. [CRUD Operations Best Practices](#crud-operations-best-practices)
5. [Enhanced Dependencies](#enhanced-dependencies)
6. [API Response Wrappers](#api-response-wrappers)
7. [Advanced Router Implementation](#advanced-router-implementation)
8. [Production Ready Examples](#production-ready-examples)

---

## Enhanced Configuration

### Hierarchical Configuration with Environments

```python
# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class BaseConfig(BaseSettings):
    """Base configuration"""
    app_name: str = "Task Manager API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    debug: bool = True
    database_url: str = "sqlite:///./dev.db"
    secret_key: str = "dev-secret-key-change-in-production"
    log_level: str = "DEBUG"
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000"
    ]

class TestingConfig(BaseConfig):
    """Testing configuration"""
    debug: bool = True
    database_url: str = "sqlite:///:memory:"
    secret_key: str = "test-secret-key"
    log_level: str = "DEBUG"
    allowed_origins: list[str] = ["*"]

class ProductionConfig(BaseConfig):
    """Production configuration"""
    debug: bool = False
    database_url: str  # Must be set in environment
    secret_key: str    # Must be set in environment
    log_level: str = "INFO"
    allowed_origins: list[str]  # Must be set in environment
    
    class Config(BaseConfig.Config):
        validate_default = True

def get_config() -> BaseConfig:
    """Get configuration based on environment"""
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()

@lru_cache()
def get_settings() -> BaseConfig:
    """Cache settings"""
    return get_config()
```

---

## Improved Database Models

### Advanced SQLAlchemy Models with Mixins

```python
# app/models/mixins.py
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin

@declarative_mixin
class TimestampMixin:
    """Add created_at and updated_at timestamps"""
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.mixins import TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.username}>"

# app/models/task.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.mixins import TimestampMixin

class Task(Base, TimestampMixin):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    priority = Column(Integer, default=0)
    
    # Relationships
    owner = relationship("User", back_populates="tasks")
    
    def __repr__(self):
        return f"<Task {self.title}>"
```

---

## Advanced Schemas with Validation

### Pydantic Schemas with Custom Validators

```python
# app/schemas/user.py
from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_-]*$",
        description="Username (alphanumeric, underscore, hyphen only)"
    )
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password must be at least 8 characters"
    )
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# app/schemas/task.py
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Task title"
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Task description"
    )
    priority: TaskPriority = TaskPriority.MEDIUM

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255
    )
    description: Optional[str] = Field(
        None,
        max_length=2000
    )
    completed: Optional[bool] = None
    priority: Optional[TaskPriority] = None

class Task(TaskBase):
    id: int
    owner_id: int
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Pagination schema
class PaginatedResponse(BaseModel):
    items: list
    total: int
    skip: int
    limit: int
    
    @property
    def total_pages(self) -> int:
        return (self.total + self.limit - 1) // self.limit
```

---

## CRUD Operations Best Practices

### Modularized CRUD with Error Handling

```python
# app/crud/base.py
from typing import TypeVar, Generic, Type
from sqlalchemy.orm import Session
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base CRUD operations"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: int) -> ModelType | None:
        """Get record by ID"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> list[ModelType]:
        """Get multiple records"""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(
        self, 
        db: Session, 
        obj_in: CreateSchemaType
    ) -> ModelType:
        """Create new record"""
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: UpdateSchemaType
    ) -> ModelType:
        """Update record"""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> bool:
        """Delete record"""
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

# app/crud/user.py
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.crud.base import CRUDBase
from app.dependencies import get_password_hash

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """User CRUD operations"""
    
    def get_by_username(self, db: Session, username: str) -> User | None:
        """Get user by username"""
        return db.query(self.model).filter(
            self.model.username == username
        ).first()
    
    def create(self, db: Session, obj_in: UserCreate) -> User:
        """Create new user with hashed password"""
        create_data = obj_in.model_dump()
        create_data.pop("password")
        create_data["hashed_password"] = get_password_hash(obj_in.password)
        db_obj = self.model(**create_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def authenticate(
        self, 
        db: Session, 
        username: str, 
        password: str
    ) -> User | None:
        """Authenticate user"""
        from app.dependencies import verify_password
        
        user = self.get_by_username(db, username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

# app/crud/task.py
from sqlalchemy.orm import joinedload
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.crud.base import CRUDBase

class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    """Task CRUD operations"""
    
    def get_by_user(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> list[Task]:
        """Get tasks for user"""
        return db.query(self.model).filter(
            self.model.owner_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_completed_tasks(
        self,
        db: Session,
        user_id: int
    ) -> list[Task]:
        """Get completed tasks for user"""
        return db.query(self.model).filter(
            self.model.owner_id == user_id,
            self.model.completed == True
        ).all()
    
    def get_by_user_and_id(
        self,
        db: Session,
        task_id: int,
        user_id: int
    ) -> Task | None:
        """Get task by ID and user"""
        return db.query(self.model).filter(
            self.model.id == task_id,
            self.model.owner_id == user_id
        ).first()

# app/crud/__init__.py
from app.crud.user import CRUDUser
from app.crud.task import CRUDTask
from app.models.user import User
from app.models.task import Task
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.task import TaskCreate, TaskUpdate

user = CRUDUser(User)
task = CRUDTask(Task)
```

---

## Enhanced Dependencies

### Advanced Authentication & Dependencies

```python
# app/dependencies.py
from datetime import datetime, timedelta, timezone
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import logging

from app.database import SessionLocal
from app.models.user import User
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    return pwd_context.hash(password)

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    logger.info(f"Created access token for user {data.get('sub')}")
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        
        if payload.get("type") != "access":
            raise AuthenticationError("Invalid token type")
        
        return payload
    except JWTError as e:
        logger.error(f"Token verification failed: {e}")
        raise AuthenticationError("Invalid token")

def get_db() -> Generator:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    try:
        payload = verify_token(token)
        username: str = payload.get("sub")
        
        if username is None:
            raise AuthenticationError("Invalid token payload")
    except JWTError:
        raise AuthenticationError()
    
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        logger.warning(f"User not found: {username}")
        raise AuthenticationError("User not found")
    
    if not user.is_active:
        raise AuthenticationError("User is inactive")
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

---

## API Response Wrappers

### Standardized Response Format

```python
# app/schemas/response.py
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
from datetime import datetime

T = TypeVar('T')

class SuccessResponse(BaseModel, Generic[T]):
    """Generic success response"""
    success: bool = True
    data: T
    message: Optional[str] = None
    timestamp: datetime = datetime.utcnow()

class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: str
    error_code: str
    timestamp: datetime = datetime.utcnow()

class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response"""
    success: bool = True
    data: list[T]
    pagination: dict
    timestamp: datetime = datetime.utcnow()
```

---

## Advanced Router Implementation

### Complete Router with Best Practices

```python
# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import logging

from app import schemas, crud
from app.database import get_db
from app.dependencies import (
    create_access_token,
    verify_password,
    get_password_hash,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post(
    "/register",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user"
)
def register(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user account"""
    
    # Check if user exists
    existing_user = crud.user.get_by_username(db, user_in.username)
    if existing_user:
        logger.warning(f"Registration attempt with existing username: {user_in.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create user
    user = crud.user.create(db, user_in)
    logger.info(f"New user registered: {user.username}")
    return user

@router.post(
    "/login",
    response_model=dict,
    summary="Login with credentials"
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login with username and password"""
    
    # Authenticate user
    user = crud.user.authenticate(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in: {user.username}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=schemas.User)
async def get_me(current_user = Depends(get_current_user)):
    """Get current user profile"""
    return current_user

# routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging

from app import schemas, crud
from app.database import get_db
from app.dependencies import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get(
    "/",
    response_model=dict,
    summary="List user tasks"
)
def read_tasks(
    skip: int = Query(0, ge=0, description="Items to skip"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    completed: bool | None = Query(None, description="Filter by completion status"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all tasks for current user with pagination"""
    
    query = db.query(crud.Task).filter(crud.Task.owner_id == current_user.id)
    
    if completed is not None:
        query = query.filter(crud.Task.completed == completed)
    
    total = query.count()
    tasks = query.offset(skip).limit(limit).all()
    
    return {
        "items": tasks,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.post(
    "/",
    response_model=schemas.Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create new task"
)
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new task"""
    task = crud.task.create(
        db,
        TaskCreate(**task_in.model_dump(), owner_id=current_user.id)
    )
    logger.info(f"Task created: {task.id} by user {current_user.username}")
    return task

@router.put(
    "/{task_id}",
    response_model=schemas.Task,
    summary="Update task"
)
def update_task(
    task_id: int,
    task_in: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a task"""
    task = crud.task.get_by_user_and_id(db, task_id, current_user.id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    task = crud.task.update(db, task, task_in)
    logger.info(f"Task updated: {task.id}")
    return task

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a task"""
    task = crud.task.get_by_user_and_id(db, task_id, current_user.id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    crud.task.delete(db, task_id)
    logger.info(f"Task deleted: {task_id}")
```

---

## Production Ready Examples

### Main Application Setup

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
import logging

from app.config import get_settings
from app.database import Base, engine
from routers import auth, tasks
from app.logging_config import setup_logging

# Setup logging
logger = setup_logging()

# Get settings
settings = get_settings()

# Create app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# Add middleware
app.add_middleware(GZIPMiddleware, minimum_size=1000)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "*.example.com"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"]
)

# Create tables
@app.on_event("startup")
def startup_event():
    """Initialize database"""
    Base.metadata.create_all(bind=engine)
    logger.info("Application startup complete")

@app.on_event("shutdown")
def shutdown_event():
    """Cleanup"""
    logger.info("Application shutdown")

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)

# Health check
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

This guide provides practical implementations of FastAPI best practices for your Task Manager project!
