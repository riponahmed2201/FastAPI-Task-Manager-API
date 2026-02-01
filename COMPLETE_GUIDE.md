# Complete Guide - Architecture, Best Practices & Deployment

Comprehensive guide covering everything from architecture details to deployment and best practices.

## 📚 Table of Contents

1. [Architecture Deep Dive](#architecture-deep-dive)
2. [Project Structure](#project-structure)
3. [Best Practices](#best-practices)
4. [Development Workflow](#development-workflow)
5. [Testing](#testing)
6. [Deployment](#deployment)
7. [Performance Optimization](#performance-optimization)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Topics](#advanced-topics)

---

## Architecture Deep Dive

### Layered Architecture Pattern

```
┌─────────────────────────────────────────────────────────┐
│  HTTP Layer (routers/)                                  │
│  ├── auth.py       - Authentication endpoints          │
│  └── tasks.py      - Task management endpoints          │
└────────────────────┬────────────────────────────────────┘
                     │
┌─────────────────────▼────────────────────────────────────┐
│  Business Logic Layer (services/)                       │
│  ├── user_service.py   - User business logic           │
│  └── task_service.py   - Task business logic           │
└────────────────────┬────────────────────────────────────┘
                     │
┌─────────────────────▼────────────────────────────────────┐
│  Data Access Layer (repositories/)                      │
│  └── repositories.py   - Database queries               │
└────────────────────┬────────────────────────────────────┘
                     │
┌─────────────────────▼────────────────────────────────────┐
│  Database Layer (models/ + database.py)                │
│  ├── models.py     - SQLAlchemy ORM models              │
│  └── database.py   - Database configuration             │
└────────────────────┬────────────────────────────────────┘
                     │
┌─────────────────────▼────────────────────────────────────┐
│  SQLite Database                                        │
└─────────────────────────────────────────────────────────┘
```

### Request Flow Example

**User Registration Request:**

```
1. POST /auth/register
   ↓ (routers/auth.py)
   - Receive HTTP request
   - Validate schema with Pydantic
   ↓
2. UserService.register_user()
   ↓ (app/services/user_service.py)
   - Validate business rules
   - Check username exists
   - Hash password
   ↓
3. UserRepository.create()
   ↓ (app/repositories.py)
   - Execute database INSERT
   ↓
4. Database
   ↓
5. Return 201 Created with User object
```

### Benefits of Layered Architecture

✅ **Separation of Concerns** - Each layer has single responsibility  
✅ **Testability** - Services testable without HTTP/DB  
✅ **Reusability** - Repositories used by multiple services  
✅ **Maintainability** - Easy to locate and modify logic  
✅ **Scalability** - Easy to add new features  
✅ **Flexibility** - Easy to swap implementations (DB, cache, etc.)  

---

## Project Structure

### Full Directory Tree

```
task-manager-app/
├── app/                          # Core application
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry
│   ├── database.py               # SQLAlchemy configuration
│   ├── models.py                 # ORM models (User, Task)
│   ├── repositories.py           # Data access layer
│   ├── schemas/                  # Pydantic validation schemas
│   │   ├── __init__.py
│   │   ├── user_schema.py        # User validation
│   │   └── task_schema.py        # Task validation
│   └── services/                 # Business logic layer
│       ├── __init__.py
│       ├── user_service.py       # User operations
│       └── task_service.py       # Task operations
│
├── routers/                      # API route handlers
│   ├── __init__.py
│   ├── auth.py                   # /auth endpoints
│   └── tasks.py                  # /tasks endpoints
│
├── core/                         # Cross-cutting concerns
│   ├── __init__.py
│   ├── config.py                 # Core configuration
│   ├── logging/                  # Logging setup
│   │   └── __init__.py           # Logger configuration
│   └── security/                 # Security utilities
│       ├── __init__.py
│       └── auth.py               # JWT, password hashing
│
├── config/                       # Configuration management
│   ├── __init__.py
│   └── settings.py               # Pydantic BaseSettings
│
├── utils/                        # Helper utilities
│   └── __init__.py               # Utility functions
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest configuration
│   ├── unit/                    # Unit tests
│   │   ├── __init__.py
│   │   ├── test_user_service.py
│   │   └── test_task_service.py
│   └── integration/             # Integration tests
│       └── __init__.py
│
├── logs/                         # Application logs (generated)
│
├── .env                          # Environment variables
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── pytest.ini                    # Pytest configuration
├── README.md                     # Project overview
└── COMPLETE_GUIDE.md            # This file
```

### Layer Responsibilities

#### routers/ - HTTP Layer
```python
# routers/auth.py
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Accept HTTP request
    # 2. Validate with Pydantic schema
    # 3. Call service
    # 4. Return HTTP response
    return UserService.register_user(db, user.username, user.password)
```

**Responsibilities:**
- Parse HTTP requests
- Validate with Pydantic schemas
- Call appropriate services
- Return HTTP responses
- Handle HTTP status codes
- No business logic

#### services/ - Business Logic Layer
```python
# app/services/user_service.py
class UserService:
    @staticmethod
    def register_user(db, username, password):
        # 1. Validate username length
        # 2. Check if user exists
        # 3. Hash password
        # 4. Call repository
        # 5. Return user object
        if len(username) < 3:
            raise ValueError("Username too short")
        if UserRepository.get_by_username(db, username):
            raise ValueError("User exists")
        hashed = get_password_hash(password)
        return UserRepository.create(db, user_obj)
```

**Responsibilities:**
- Implement business rules
- Validate business logic
- Orchestrate repositories
- Handle exceptions
- No HTTP knowledge
- No database queries

#### repositories/ - Data Access Layer
```python
# app/repositories.py
class UserRepository:
    @staticmethod
    def create(db, user):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
```

**Responsibilities:**
- Execute database queries
- Handle ORM operations
- Manage transactions
- Return entities
- No business logic
- Reusable methods

#### models/ - Database Layer
```python
# app/models.py
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    tasks = relationship("Task", back_populates="owner")
```

**Responsibilities:**
- Define database schema
- Define relationships
- ORM entity definitions
- No business logic
- No queries

---

## Best Practices

### 1. Code Organization

✅ **DO:**
- Group related functionality in same module
- Use meaningful file names
- Keep functions small and focused
- Use type hints throughout

❌ **DON'T:**
- Mix concerns in single file
- Use vague function names
- Create massive functions
- Ignore type hints

### 2. Error Handling

```python
# ✅ Good
@router.post("/register")
def register(user: UserCreate, db: Session):
    try:
        return UserService.register_user(db, user.username, user.password)
    except ValueError as e:
        logger.warning(f"Registration failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal error")

# ❌ Bad
@router.post("/register")
def register(user: UserCreate, db: Session):
    return UserService.register_user(db, user.username, user.password)
```

### 3. Validation

```python
# ✅ Good - Multiple levels
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

class UserService:
    @staticmethod
    def register_user(db, username, password):
        if not username or len(username.strip()) == 0:
            raise ValueError("Username empty")
        # Additional business validation

# ❌ Bad - Only schema validation
@router.post("/register")
def register(user: UserCreate, db: Session):
    return create_user(db, user)
```

### 4. Database Transactions

```python
# ✅ Good
def create_task_with_notification(db: Session, task_data):
    try:
        task = TaskRepository.create(db, task_data)
        NotificationRepository.create(db, task.id)
        db.commit()
        return task
    except Exception as e:
        db.rollback()
        raise

# ❌ Bad
def create_task_with_notification(db: Session, task_data):
    task = TaskRepository.create(db, task_data)
    NotificationRepository.create(db, task.id)  # May fail, task already in DB
```

### 5. Logging

```python
# ✅ Good
from core.logging import logger

@router.post("/register")
def register(user: UserCreate, db: Session):
    logger.info(f"Registration attempt: {user.username}")
    try:
        result = UserService.register_user(db, user.username, user.password)
        logger.info(f"User registered: {user.username}")
        return result
    except ValueError as e:
        logger.warning(f"Registration failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# ❌ Bad
@router.post("/register")
def register(user: UserCreate, db: Session):
    print(f"Registering {user.username}")  # Use logger!
    return UserService.register_user(db, user.username, user.password)
```

### 6. Security

```python
# ✅ Good
# Use dependencies for auth
@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# Hash passwords
hashed = get_password_hash(password)

# Validate tokens
user = verify_token(token)

# ❌ Bad
# Store plain passwords
user.password = password  # Never!

# No auth on sensitive endpoints
@router.get("/admin/users")
def get_all_users(db: Session):
    return db.query(User).all()  # Anyone can access!

# Ignore token validation
def get_user_from_token(token):
    # No validation
    return decode(token)
```

### 7. Testing

```python
# ✅ Good - Test business logic
def test_register_user_duplicate():
    with Session(engine) as db:
        UserService.register_user(db, "john", "password123")
        with pytest.raises(ValueError):
            UserService.register_user(db, "john", "password456")

# ✅ Good - Test with fixtures
@pytest.fixture
def user(db):
    return UserService.register_user(db, "john", "password123")

def test_create_task(db, user):
    task = TaskService.create_task(db, user.id, "Title")
    assert task.owner_id == user.id

# ❌ Bad - Testing through HTTP
def test_register():
    response = client.post("/auth/register", ...)
    # Too many layers, slow, fragile
```

---

## Development Workflow

### Adding New Feature

1. **Design Schema**
   ```python
   # app/schemas/comment_schema.py
   class CommentCreate(BaseModel):
       text: str = Field(..., min_length=1, max_length=500)
       task_id: int
   ```

2. **Create Model**
   ```python
   # Add to app/models.py
   class Comment(Base):
       __tablename__ = "comment"
       id = Column(Integer, primary_key=True)
       text = Column(String)
       task_id = Column(Integer, ForeignKey("task.id"))
   ```

3. **Create Repository Methods**
   ```python
   # Add to app/repositories.py
   class CommentRepository:
       @staticmethod
       def create(db, comment):
           db.add(comment)
           db.commit()
           db.refresh(comment)
           return comment
   ```

4. **Create Service**
   ```python
   # app/services/comment_service.py
   class CommentService:
       @staticmethod
       def create_comment(db, task_id, text, user_id):
           if len(text.strip()) == 0:
               raise ValueError("Comment empty")
           comment = Comment(text=text, task_id=task_id)
           return CommentRepository.create(db, comment)
   ```

5. **Create Router**
   ```python
   # routers/comments.py
   @router.post("/tasks/{task_id}/comments")
   def create_comment(task_id: int, comment: CommentCreate, ...):
       return CommentService.create_comment(db, task_id, comment.text, user_id)
   ```

6. **Add Tests**
   ```python
   # tests/unit/test_comment_service.py
   def test_create_comment(db, user, task):
       comment = CommentService.create_comment(db, task.id, "Good task", user.id)
       assert comment.task_id == task.id
   ```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific file
pytest tests/unit/test_user_service.py

# Run with coverage
pytest --cov=app tests/

# Run with verbose output
pytest -v tests/

# Run specific test
pytest tests/unit/test_user_service.py::TestUserService::test_register_user_success
```

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── unit/
│   ├── test_user_service.py
│   └── test_task_service.py
└── integration/
    ├── test_auth_routes.py  # Route integration tests
    └── test_task_routes.py
```

### Example Tests

```python
# tests/conftest.py
@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

# tests/unit/test_user_service.py
class TestUserService:
    def test_register_success(self, db):
        user = UserService.register_user(db, "john", "pass123")
        assert user.username == "john"
    
    def test_register_duplicate_fails(self, db):
        UserService.register_user(db, "john", "pass123")
        with pytest.raises(ValueError):
            UserService.register_user(db, "john", "pass456")
```

---

## Deployment

### Development Server

```bash
python -m uvicorn app.main:app --reload --port 8000
```

### Production Server (Gunicorn)

```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app

# With configuration
gunicorn -w 4 \
  -b 0.0.0.0:8000 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile - \
  app.main:app
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app.main:app"]
```

```bash
# Build image
docker build -t task-manager .

# Run container
docker run -p 8000:8000 -e SECRET_KEY=your-key task-manager
```

### Nginx Configuration

```nginx
upstream app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /app/static;
    }
}
```

### Environment Setup

```bash
# Production .env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=your-production-secret-key-min-32-chars
DEBUG=False
LOG_LEVEL=INFO
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

---

## Performance Optimization

### 1. Database Indexing

```python
# app/models.py
class User(Base):
    __tablename__ = "user"
    username = Column(String, unique=True, index=True)  # Add index
    created_at = Column(DateTime, index=True)

class Task(Base):
    __tablename__ = "task"
    owner_id = Column(Integer, ForeignKey("user.id"), index=True)
    completed = Column(Boolean, index=True)
```

### 2. Query Optimization

```python
# ✅ Good - Use select() for better control
from sqlalchemy import select

tasks = db.execute(
    select(Task).where(Task.owner_id == user_id).limit(10)
).scalars()

# ❌ Bad - Inefficient query
tasks = db.query(Task).filter(Task.owner_id == user_id).all()
```

### 3. Connection Pooling

```python
# app/database.py
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
)
```

### 4. Caching

```python
# ✅ Cache user lookups
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_user_cached(user_id: int):
    # Cached for 1000 most recent lookups
    return UserRepository.get_by_id(db, user_id)
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Port already in use | Another app using port | Use `--port 8001` |
| Database locked | SQLite access conflict | Delete db file, restart |
| Import errors | Missing dependencies | `pip install -r requirements.txt` |
| Token invalid | Expired or tampered | Login again |
| Slow queries | Missing indexes | Add indexes to columns |
| CORS errors | Origin not allowed | Update CORS settings |

### Debug Mode

```bash
# Enable debug logging
export DEBUG=True
export LOG_LEVEL=DEBUG

# Run with debug
python -m uvicorn app.main:app --reload
```

### Check Logs

```bash
# Tail logs
tail -f logs/task_manager.log

# Search logs
grep "error" logs/task_manager.log

# Recent errors
tail -50 logs/task_manager.log | grep ERROR
```

---

## Advanced Topics

### 1. Database Migrations (Alembic)

```bash
# Initialize Alembic
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Add user table"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

### 2. Caching Layer

```python
# Add Redis caching
from redis import Redis

redis_client = Redis(host='localhost', port=6379, db=0)

class CachedRepository:
    @staticmethod
    def get_user(user_id):
        cached = redis_client.get(f"user:{user_id}")
        if cached:
            return json.loads(cached)
        user = UserRepository.get_by_id(db, user_id)
        redis_client.setex(f"user:{user_id}", 3600, json.dumps(user))
        return user
```

### 3. Background Tasks

```python
# Celery task
from celery import Celery

celery_app = Celery('tasks')

@celery_app.task
def send_notification(task_id):
    # Send email notification
    pass

# In router
from fastapi import BackgroundTasks

@router.post("/tasks/")
def create_task(task: TaskCreate, background_tasks: BackgroundTasks):
    new_task = TaskService.create_task(db, task)
    background_tasks.add_task(send_notification, new_task.id)
    return new_task
```

### 4. API Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/tasks/")
@limiter.limit("10/minute")
def get_tasks(request: Request, db: Session = Depends(get_db)):
    return TaskService.get_tasks(db, request.user.id)
```

---

## Monitoring & Observability

### Application Monitoring

```python
# app/main.py
from prometheus_client import Counter, Histogram

request_count = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
request_duration = Histogram('requests_duration_seconds', 'Request duration')

@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    request_count.labels(method=request.method, endpoint=request.url.path).inc()
    request_duration.observe(time.time() - start)
    return response
```

### Health Check Endpoint

```python
@app.get("/health/detailed")
def health_detailed():
    return {
        "status": "healthy",
        "database": check_database_connection(),
        "cache": check_cache_connection(),
        "disk": check_disk_space(),
    }
```

---

## Summary

This guide covers everything from basic setup to advanced production deployment. For specific questions:

1. Check README.md for quick start
2. Review ARCHITECTURE.md for design patterns
3. Check STRUCTURE.md for folder organization
4. Consult API docs at http://localhost:8000/docs

---

**Production-Ready Task Manager API**  
**Version 1.0.0 - February 2026**
