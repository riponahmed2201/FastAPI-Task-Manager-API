# Production-Ready Folder Structure

## 📁 Project Directory Structure

```
task-manager-app/
├── app/                          # Main application code
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── database.py               # Database configuration
│   ├── models.py                 # SQLAlchemy ORM models
│   ├── repositories.py           # Data access layer
│   ├── schemas/                  # Pydantic validation schemas
│   │   ├── __init__.py
│   │   ├── user_schema.py        # User schemas
│   │   └── task_schema.py        # Task schemas
│   └── services/                 # Business logic layer
│       ├── __init__.py
│       ├── user_service.py       # User service
│       └── task_service.py       # Task service
│
├── routers/                      # API route handlers
│   ├── __init__.py
│   ├── auth.py                   # Authentication routes
│   └── tasks.py                  # Task routes
│
├── core/                         # Core application functionality
│   ├── __init__.py
│   ├── config.py                 # Application configuration
│   ├── logging/                  # Logging setup
│   │   └── __init__.py
│   └── security/                 # Security utilities
│       ├── __init__.py
│       └── auth.py               # Authentication & JWT
│
├── config/                       # Configuration management
│   ├── __init__.py
│   └── settings.py               # Settings from environment
│
├── utils/                        # Utility functions
│   └── __init__.py               # Helper functions
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
├── README.md                     # Project documentation
└── STRUCTURE.md                  # This file
```

## 📚 Layer Responsibility

### 1. **routers/** - HTTP Layer
- Handles HTTP requests/responses
- Input validation via Pydantic schemas
- Returns JSON responses
- No business logic

**Files:**
- `auth.py` - User authentication endpoints
- `tasks.py` - Task management endpoints

---

### 2. **services/** - Business Logic Layer
- Implements business rules and logic
- Validation beyond schema validation
- Orchestrates repositories
- Exception handling
- No HTTP knowledge

**Files:**
- `user_service.py` - User business logic
- `task_service.py` - Task business logic

---

### 3. **repositories/** - Data Access Layer
- Database CRUD operations
- Query building
- No business logic
- Reusable data operations

**File:**
- `repositories.py` - UserRepository, TaskRepository

---

### 4. **schemas/** - Validation Layer
- Pydantic models
- Input/output validation
- Type definitions
- Documentation

**Files:**
- `user_schema.py` - User validation schemas
- `task_schema.py` - Task validation schemas

---

### 5. **models/** - Database Layer
- SQLAlchemy ORM models
- Database schema definition
- Relationships

**File:**
- `models.py` - User, Task models

---

### 6. **core/** - Cross-Cutting Concerns
- Configuration management
- Logging setup
- Security utilities
- Global concerns

**Directories:**
- `config/` - Settings from environment
- `logging/` - Logging configuration
- `security/` - Authentication & JWT

---

### 7. **utils/** - Helper Functions
- Reusable utility functions
- Common operations
- Response formatting

---

### 8. **tests/** - Quality Assurance
- Unit tests for services
- Integration tests for routes
- Test fixtures and configuration

---

## 🔄 Request Flow

```
1. HTTP Request
   ↓
2. routers/ (auth.py, tasks.py)
   - Parse request
   - Validate with schemas
   ↓
3. services/ (user_service.py, task_service.py)
   - Business logic
   - Data validation
   - Error handling
   ↓
4. repositories/ (repositories.py)
   - Data access
   - Database queries
   ↓
5. models/ (models.py)
   - ORM models
   - Database interaction
   ↓
6. HTTP Response
```

---

## 🚀 Key Features

✅ **Separation of Concerns** - Each layer has clear responsibility  
✅ **Scalability** - Easy to add new features  
✅ **Testability** - Services can be tested without HTTP  
✅ **Maintainability** - Clear code organization  
✅ **Production Ready** - Logging, error handling, configuration  

---

## 📋 File Organization Summary

| Layer | Directory | Purpose |
|-------|-----------|---------|
| HTTP | `routers/` | API endpoints |
| Business | `services/` | Business logic |
| Data | `repositories/` | Database access |
| Validation | `schemas/` | Input/output validation |
| Database | `app/models.py` | ORM models |
| Configuration | `config/`, `core/` | Settings & setup |
| Security | `core/security/` | Auth & JWT |
| Testing | `tests/` | Unit & integration tests |
| Utilities | `utils/` | Helper functions |
| Logging | `core/logging/` | Application logs |

---

## 🎯 Best Practices Applied

1. **Domain-Driven Design** - Organized around business domains
2. **Layered Architecture** - Clear separation of concerns
3. **Dependency Injection** - FastAPI dependencies for DB sessions
4. **Configuration Management** - Settings from environment
5. **Logging** - Structured logging across application
6. **Testing** - Pytest fixtures and test organization
7. **Documentation** - Clear code and folder structure
8. **Modularity** - Easy to extend and modify

---

## 🏗️ Adding New Features

To add a new domain (e.g., "Comments"):

1. **Create schema** → `app/schemas/comment_schema.py`
2. **Create model** → Add to `app/models.py`
3. **Create repository** → Add `CommentRepository` to `repositories.py`
4. **Create service** → `app/services/comment_service.py`
5. **Create router** → `routers/comments.py`
6. **Create tests** → `tests/unit/test_comment_service.py`

---

## 📦 Import Examples

```python
# ✅ Good imports
from config.settings import settings
from core.security import get_current_user, create_access_token
from app.services import UserService, TaskService
from app.schemas import User, Task, UserCreate
from app import models

# ❌ Avoid
from app.dependencies import ...  # Now in core/security
from app.schemas import ...  # Now import-able from app.schemas
```

---

**Last Updated:** February 2026  
**Version:** 1.0.0 (Production-Ready)
