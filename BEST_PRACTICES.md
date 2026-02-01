# FastAPI Task Manager - Best Practices Guide

A comprehensive guide for maintaining, extending, and deploying your Task Manager API following industry standards and best practices.

## 📋 Table of Contents

1. [Code Organization](#code-organization)
2. [Security Best Practices](#security-best-practices)
3. [Performance Optimization](#performance-optimization)
4. [Testing Strategies](#testing-strategies)
5. [Error Handling](#error-handling)
6. [Logging & Monitoring](#logging--monitoring)
7. [Deployment](#deployment)
8. [Database Management](#database-management)
9. [API Design](#api-design)
10. [Development Workflow](#development-workflow)

---

## Code Organization

### Project Structure Best Practices

```
task-manager-app/
├── app/
│   ├── __init__.py
│   ├── main.py                  # App initialization
│   ├── config.py               # Configuration (NEW)
│   ├── database.py             # Database setup
│   ├── models/                 # Models (NEW - modularized)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/                # Schemas (NEW - modularized)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── crud/                   # CRUD operations (NEW - modularized)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── dependencies.py         # Dependencies
│   └── exceptions.py           # Custom exceptions (NEW)
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   └── tasks.py
├── tests/                      # Tests (NEW)
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_tasks.py
│   └── test_database.py
├── migrations/                 # Database migrations (NEW)
├── logs/                       # Application logs (NEW)
├── .env
├── .env.example               # Environment template (NEW)
├── .gitignore
├── pytest.ini                 # Pytest config (NEW)
├── pyproject.toml             # Project config (NEW)
├── requirements.txt
├── requirements-dev.txt       # Dev dependencies (NEW)
└── docker-compose.yml         # Docker setup (NEW)
```

### Module Organization

**✅ DO:**
```python
# app/models/user.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
```

**❌ DON'T:**
```python
# Put everything in one file
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class User(Base):
    # ... user model

class Task(Base):
    # ... task model

class Permission(Base):
    # ... permission model
```

### Naming Conventions

**✅ DO:**
```python
# Clear, descriptive names
def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

# Models use PascalCase
class UserTask:
    pass

# Functions use snake_case
def create_new_task():
    pass

# Constants use UPPER_SNAKE_CASE
MAX_TASK_TITLE_LENGTH = 255
DEFAULT_PAGE_SIZE = 20
```

**❌ DON'T:**
```python
# Unclear names
def get_data(db, x):
    return db.query(User).filter(User.id == x).first()

# Inconsistent naming
class userTask:
    pass

def CreateNewTask():
    pass

# Magic numbers
if len(title) > 255:
    pass
```

---

## Security Best Practices

### 1. Environment Variables & Secrets

**✅ DO:**
```python
# app/config.py
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./tasks.db"
    )
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Validation
    if not secret_key:
        raise ValueError("SECRET_KEY environment variable must be set")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

**✅ Create .env.example:**
```
DATABASE_URL=sqlite:///./tasks.db
SECRET_KEY=your-super-secret-key-minimum-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
LOG_LEVEL=INFO
DEBUG=False
```

**❌ DON'T:**
```python
# Hardcode secrets
SECRET_KEY = "super-secret-key"
DATABASE_URL = "postgresql://user:password@localhost/db"

# Commit .env file
# .env in git
```

### 2. Password Security

**✅ DO:**
```python
# app/dependencies.py
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Use more rounds for production
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password with constant-time comparison"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password with bcrypt"""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    return pwd_context.hash(password)
```

**❌ DON'T:**
```python
# Store passwords in plain text
user.password = "plaintext"

# Use weak hashing
import hashlib
user.password = hashlib.md5(password.encode()).hexdigest()

# Allow weak passwords
def get_password_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### 3. Token Management

**✅ DO:**
```python
# app/dependencies.py
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

def create_access_token(
    data: dict, 
    expires_delta: timedelta | None = None
) -> str:
    """Create JWT token with expiration"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

**✅ DO - Token refresh pattern:**
```python
@router.post("/auth/refresh")
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
) -> dict:
    """Refresh access token using refresh token"""
    payload = verify_token(refresh_token)
    user = db.query(User).filter(
        User.id == payload.get("sub")
    ).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

**❌ DON'T:**
```python
# Never expire tokens
def create_access_token(data):
    return jwt.encode(data, SECRET_KEY)

# Store tokens in database without expiration
user.token = token
db.commit()
```

### 4. Input Validation

**✅ DO:**
```python
# app/schemas/task.py
from pydantic import BaseModel, Field, validator

class TaskCreate(BaseModel):
    title: str = Field(
        ..., 
        min_length=1, 
        max_length=255,
        description="Task title"
    )
    description: str | None = Field(
        None, 
        max_length=2000,
        description="Task description"
    )
    
    @validator('title')
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

class TaskUpdate(TaskCreate):
    title: str | None = Field(
        None, 
        min_length=1, 
        max_length=255
    )
```

**❌ DON'T:**
```python
# No validation
class TaskCreate(BaseModel):
    title: str
    description: str

# Accept user input without sanitization
@router.post("/tasks/")
def create_task(title, description):
    task = Task(title=title, description=description)
```

### 5. CORS Configuration

**✅ DO:**
```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware

# Define allowed origins explicitly
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://yourdomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Not "*"
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

**❌ DON'T:**
```python
# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Security risk
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 6. Rate Limiting

**✅ DO:**
```python
# app/main.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/tasks/")
@limiter.limit("100/minute")
def read_tasks(request: Request, ...):
    return tasks
```

---

## Performance Optimization

### 1. Database Query Optimization

**✅ DO:**
```python
# app/crud/task.py
from sqlalchemy.orm import selectinload, joinedload

def get_tasks_with_users(db: Session, user_id: int):
    """Use eager loading to prevent N+1 queries"""
    return db.query(Task).options(
        joinedload(Task.owner)
    ).filter(Task.owner_id == user_id).all()

# Use indexing in models
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), index=True)
    completed = Column(Boolean, index=True, default=False)
```

**❌ DON'T:**
```python
# N+1 queries - causes performance issues
tasks = db.query(Task).all()
for task in tasks:
    owner = db.query(User).filter(User.id == task.owner_id).first()
    print(owner.username)
```

### 2. Pagination

**✅ DO:**
```python
# app/schemas/pagination.py
from pydantic import BaseModel, Field

class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0, description="Number of items to skip")
    limit: int = Field(20, ge=1, le=100, description="Items per page")

# app/crud/task.py
def get_tasks_paginated(
    db: Session, 
    user_id: int,
    skip: int = 0,
    limit: int = 20
):
    """Get paginated tasks"""
    return db.query(Task).filter(
        Task.owner_id == user_id
    ).offset(skip).limit(limit).all()

# routers/tasks.py
@router.get("/tasks/", response_model=list[TaskSchema])
def read_tasks(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_tasks_paginated(db, current_user.id, skip, limit)
```

**❌ DON'T:**
```python
# Return all records
@router.get("/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()  # Could be millions!
```

### 3. Caching

**✅ DO:**
```python
# app/cache.py
from functools import lru_cache
import redis

# Use Redis for distributed caching
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate cache key"""
    key_parts = [prefix] + list(args)
    return ":".join(str(k) for k in key_parts)

def get_cached(key: str, ttl: int = 300):
    """Get value from cache"""
    return redis_client.get(key)

def set_cache(key: str, value: str, ttl: int = 300):
    """Set cache with TTL"""
    redis_client.setex(key, ttl, value)
```

### 4. Async Operations

**✅ DO:**
```python
# Use async/await for I/O operations
@router.get("/tasks/")
async def read_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Simulate async operation
    tasks = await get_tasks_async(db, current_user.id)
    return tasks
```

---

## Testing Strategies

### 1. Setup Test Configuration

**✅ DO:**
```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
from fastapi.testclient import TestClient

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base.metadata.create_all(bind=engine)

@pytest.fixture
def db():
    """Provide test database"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db):
    """Provide test client"""
    def override_get_db():
        return db
    
    from app.dependencies import get_db
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)
    
    app.dependency_overrides.clear()
```

### 2. Authentication Tests

**✅ DO:**
```python
# tests/test_auth.py
import pytest

def test_register_user(client):
    """Test user registration"""
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_register_duplicate_username(client):
    """Test duplicate username rejection"""
    client.post(
        "/auth/register",
        json={"username": "testuser", "password": "password123"}
    )
    
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "password": "different"}
    )
    assert response.status_code == 400

def test_login_user(client):
    """Test user login"""
    # Register first
    client.post(
        "/auth/register",
        json={"username": "testuser", "password": "password123"}
    )
    
    # Login
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials(client):
    """Test invalid login"""
    response = client.post(
        "/auth/login",
        data={"username": "wrong", "password": "wrong"}
    )
    assert response.status_code == 401
```

### 3. Task Tests

**✅ DO:**
```python
# tests/test_tasks.py
import pytest

@pytest.fixture
def auth_headers(client):
    """Get authentication headers"""
    client.post(
        "/auth/register",
        json={"username": "testuser", "password": "password123"}
    )
    
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "password123"}
    )
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_task(client, auth_headers):
    """Test task creation"""
    response = client.post(
        "/tasks/",
        json={
            "title": "Test Task",
            "description": "Test Description"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_get_tasks_unauthorized(client):
    """Test unauthorized access"""
    response = client.get("/tasks/")
    assert response.status_code == 401

def test_update_task(client, auth_headers):
    """Test task update"""
    # Create task
    create_response = client.post(
        "/tasks/",
        json={"title": "Original", "description": "Original"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    # Update task
    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated", "description": "Updated"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"

def test_delete_task(client, auth_headers):
    """Test task deletion"""
    # Create task
    create_response = client.post(
        "/tasks/",
        json={"title": "To Delete"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    # Delete task
    response = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
```

### 4. Run Tests

**✅ DO:**
```bash
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# requirements-dev.txt
pytest==7.4.0
pytest-cov==4.1.0
pytest-asyncio==0.21.0

# Run tests
pytest
pytest -v  # Verbose
pytest --cov=app  # With coverage
pytest -k test_auth  # Specific tests
```

---

## Error Handling

### 1. Custom Exceptions

**✅ DO:**
```python
# app/exceptions.py
from fastapi import HTTPException, status

class TaskManagerException(Exception):
    """Base exception for task manager"""
    pass

class UserNotFoundError(TaskManagerException):
    """User not found"""
    pass

class TaskNotFoundError(TaskManagerException):
    """Task not found"""
    pass

class UnauthorizedError(TaskManagerException):
    """Unauthorized access"""
    pass

# Usage
@router.get("/tasks/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise TaskNotFoundError("Task not found")
    
    if task.owner_id != current_user.id:
        raise UnauthorizedError("Not authorized")
    
    return task
```

### 2. Exception Handlers

**✅ DO:**
```python
# app/main.py
from app.exceptions import TaskManagerException

@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.exception_handler(UnauthorizedError)
async def unauthorized_handler(request, exc):
    return JSONResponse(
        status_code=403,
        content={"detail": "Not authorized"}
    )

@app.exception_handler(TaskManagerException)
async def task_manager_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

### 3. Validation Error Handling

**✅ DO:**
```python
# app/main.py
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Handle validation errors"""
    return JSONResponse(
        status_code=422,
        content={
            "detail": [
                {
                    "loc": error["loc"],
                    "msg": error["msg"],
                    "type": error["type"]
                }
                for error in exc.errors()
            ]
        }
    )
```

---

## Logging & Monitoring

### 1. Structured Logging

**✅ DO:**
```python
# app/logging_config.py
import logging
import json
from logging.handlers import RotatingFileHandler

class JSONFormatter(logging.Formatter):
    """JSON formatter for logs"""
    
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

def setup_logging():
    """Setup application logging"""
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    
    # File handler
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(JSONFormatter())
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# app/main.py
logger = setup_logging()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests"""
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
```

### 2. Health Checks

**✅ DO:**
```python
# app/main.py
@app.get("/health")
async def health_check():
    """Application health check"""
    try:
        # Check database
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }

@app.get("/metrics")
async def metrics():
    """Application metrics"""
    return {
        "users": db.query(User).count(),
        "tasks": db.query(Task).count(),
        "completed_tasks": db.query(Task).filter(Task.completed).count()
    }
```

---

## Deployment

### 1. Production Configuration

**✅ DO:**
```python
# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "Task Manager API"
    debug: bool = False
    
    # Database
    database_url: str
    database_pool_size: int = 20
    database_max_overflow: int = 40
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: list[str] = []
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    """Get cached settings"""
    return Settings()
```

### 2. Docker Deployment

**✅ DO:**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: taskmanager
      POSTGRES_USER: taskuser
      POSTGRES_PASSWORD: securepassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://taskuser:securepassword@db:5432/taskmanager
      SECRET_KEY: your-secret-key
    depends_on:
      - db
    volumes:
      - .:/app

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### 3. Gunicorn Production Server

**✅ DO:**
```bash
# requirements.txt additions
gunicorn==21.2.0
uvicorn[standard]==0.23.2

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app

# Or with configuration file
# gunicorn_config.py
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 120
keepalive = 5
```

### 4. Nginx Reverse Proxy

**✅ DO:**
```nginx
# nginx.conf
upstream app {
    server web:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    client_max_body_size 10M;

    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Database Management

### 1. Database Migrations with Alembic

**✅ DO:**
```bash
# Install Alembic
pip install alembic

# Initialize migrations
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Add users table"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

```python
# alembic/env.py
from app.config import settings
from app.database import Base

sqlalchemy.url = settings.database_url

target_metadata = Base.metadata

def run_migrations_online() -> None:
    """Run migrations online"""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.database_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

### 2. Backup Strategy

**✅ DO:**
```bash
# Backup PostgreSQL
pg_dump taskmanager > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
psql taskmanager < backup_20240201_120000.sql

# Automated backup with cron
0 2 * * * pg_dump taskmanager | gzip > /backups/backup_$(date +\%Y\%m\%d).sql.gz
```

### 3. Connection Pooling

**✅ DO:**
```python
# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool, QueuePool

# Production: Use QueuePool with proper settings
engine = create_engine(
    database_url,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,  # Test connections
    pool_recycle=3600,   # Recycle connections every hour
    echo=False
)

# Development: Use NullPool (no pooling)
engine = create_engine(
    database_url,
    poolclass=NullPool,
    echo=True
)
```

---

## API Design

### 1. RESTful Conventions

**✅ DO:**
```python
# Follow HTTP verb conventions
@router.get("/tasks/")              # List - GET
@router.post("/tasks/")             # Create - POST
@router.get("/tasks/{id}")          # Retrieve - GET
@router.put("/tasks/{id}")          # Replace - PUT
@router.patch("/tasks/{id}")        # Partial update - PATCH
@router.delete("/tasks/{id}")       # Delete - DELETE
```

### 2. Response Models

**✅ DO:**
```python
# app/schemas/task.py
from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str | None = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

class Task(TaskBase):
    id: int
    owner_id: int
    completed: bool
    
    class Config:
        from_attributes = True

# app/routers/tasks.py
@router.get("/tasks/", response_model=list[Task])
def read_tasks(...):
    pass

@router.post("/tasks/", response_model=Task, status_code=201)
def create_task(...):
    pass
```

### 3. API Versioning

**✅ DO:**
```python
# app/main.py
from fastapi import APIRouter

# Create versioned routers
api_v1 = APIRouter(prefix="/api/v1")
api_v2 = APIRouter(prefix="/api/v2")

# Include routers
app.include_router(api_v1)
app.include_router(api_v2)

# routers/v1/tasks.py
from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
def list_tasks_v1(...):
    pass

# routers/v2/tasks.py
@router.get("/")
def list_tasks_v2(...):
    # Improved version
    pass
```

### 4. Error Response Format

**✅ DO:**
```python
# Consistent error responses
{
    "detail": "Error message",
    "error_code": "RESOURCE_NOT_FOUND",
    "timestamp": "2024-02-01T12:00:00Z"
}

# app/main.py
from pydantic import BaseModel
from datetime import datetime

class ErrorResponse(BaseModel):
    detail: str
    error_code: str
    timestamp: datetime = datetime.utcnow()

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            detail=str(exc),
            error_code="INTERNAL_SERVER_ERROR"
        ).dict()
    )
```

---

## Development Workflow

### 1. Git Best Practices

**✅ DO:**
```bash
# Use meaningful commit messages
git commit -m "feat: add task completion status update"
git commit -m "fix: resolve N+1 query in task retrieval"
git commit -m "docs: update API documentation"

# Use feature branches
git checkout -b feature/task-filtering
git checkout -b fix/auth-token-validation

# Keep commits atomic and logical
# One feature = one commit
# Never mix features in one commit
```

### 2. Code Review Checklist

**✅ DO:**
- [ ] Code follows project style guide
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No hardcoded secrets
- [ ] Error handling implemented
- [ ] Performance considerations addressed
- [ ] Security best practices followed

### 3. Pre-commit Hooks

**✅ DO:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black

  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.4.1
    hooks:
      - id: mypy

# Install
pre-commit install

# Run manually
pre-commit run --all-files
```

### 4. CI/CD Pipeline

**✅ DO:**
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.9, "3.10", "3.11"]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Lint with flake8
        run: flake8 app tests
      
      - name: Format check with black
        run: black --check app tests
      
      - name: Type check with mypy
        run: mypy app
      
      - name: Run tests
        run: pytest --cov=app tests/
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Summary: Best Practices Checklist

### Security ✅
- [ ] Use environment variables for secrets
- [ ] Hash passwords with bcrypt
- [ ] Implement token expiration
- [ ] Validate all input
- [ ] Use specific CORS origins
- [ ] Implement rate limiting
- [ ] Use HTTPS in production
- [ ] Regular security audits

### Performance ✅
- [ ] Optimize database queries (prevent N+1)
- [ ] Implement pagination
- [ ] Use caching strategy
- [ ] Database connection pooling
- [ ] Async operations
- [ ] Monitor response times

### Testing ✅
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests
- [ ] Authentication tests
- [ ] Edge case testing
- [ ] Performance tests
- [ ] Security tests

### Code Quality ✅
- [ ] Type hints throughout
- [ ] Consistent naming conventions
- [ ] Modular structure
- [ ] DRY principle
- [ ] SOLID principles
- [ ] Documentation

### Deployment ✅
- [ ] Environment-specific configs
- [ ] Database migrations
- [ ] Health checks
- [ ] Logging and monitoring
- [ ] Graceful error handling
- [ ] Backup strategies

---

**Remember**: Best practices evolve with time. Stay updated with:
- FastAPI updates
- Security advisories
- Performance benchmarks
- Industry standards

Happy coding! 🚀
