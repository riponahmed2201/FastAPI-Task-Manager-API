# Task Manager API - Production Ready

A modern, scalable Task Management API built with FastAPI, SQLAlchemy, and JWT authentication. Follows enterprise architecture patterns and best practices.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
# 1. Navigate to project
cd task-manager-app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start development server
python -m uvicorn app.main:app --reload --port 8000

# 4. Access API
# API Docs: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

---

## 🏗️ Architecture

### Layered Architecture

```
HTTP Request
    ↓
routers/ (HTTP Layer)
    ↓
services/ (Business Logic)
    ↓
repositories/ (Data Access)
    ↓
models/ (Database)
```

### Folder Structure

```
task-manager-app/
├── app/
│   ├── main.py              # FastAPI app
│   ├── database.py          # DB config
│   ├── models.py            # SQLAlchemy models
│   ├── repositories.py      # Data access layer
│   ├── schemas/             # Pydantic schemas
│   │   ├── user_schema.py
│   │   └── task_schema.py
│   └── services/            # Business logic
│       ├── user_service.py
│       └── task_service.py
├── routers/                 # API routes
│   ├── auth.py
│   └── tasks.py
├── core/                    # Core functionality
│   ├── config.py
│   ├── logging/
│   └── security/
├── config/                  # Settings
├── utils/                   # Helpers
├── tests/                   # Test suite
└── logs/                    # Generated logs
```

---

## 🔐 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login & get token |
| GET | `/auth/me` | Get current user |
| GET | `/auth/statistics` | Get user statistics |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks/` | List all tasks |
| POST | `/tasks/` | Create task |
| GET | `/tasks/{id}` | Get task |
| PUT | `/tasks/{id}` | Update task |
| PATCH | `/tasks/{id}/complete` | Mark complete |
| PATCH | `/tasks/{id}/incomplete` | Mark incomplete |
| DELETE | `/tasks/{id}` | Delete task |
| GET | `/tasks/statistics/summary` | Task statistics |

---

## 📝 Usage Examples

### Register & Login
```bash
# Register
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"pass123"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=pass123"
```

### Create Task
```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk","description":"2% milk"}'
```

### List Tasks
```bash
curl -X GET "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## ⚙️ Configuration

Edit `.env`:
```env
DATABASE_URL=sqlite:///./task_manager.db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
```

Edit `config/settings.py` for more options.

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/unit/test_user_service.py

# With coverage
pytest --cov=app tests/
```

---

## 📚 Full Documentation

**See COMPLETE_GUIDE.md** for:
- Detailed architecture
- Best practices
- Deployment guide
- Advanced features
- Troubleshooting
- Contributing guidelines

---

## 🔒 Security

✅ JWT authentication  
✅ Password hashing with bcrypt  
✅ Input validation with Pydantic  
✅ CORS protection  
✅ SQL injection protection via SQLAlchemy ORM  

⚠️ For production:
- Change SECRET_KEY
- Use PostgreSQL instead of SQLite
- Enable HTTPS/TLS
- Add rate limiting
- Enable only necessary CORS origins

---

## 🚀 Production Deployment

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

See **COMPLETE_GUIDE.md** for Docker, Nginx, and cloud deployment.

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | Use `--port 8001` or kill process |
| Database locked | Delete `task_manager.db` and restart |
| Import errors | `pip install -r requirements.txt` |
| Auth failures | Check token in header: `Authorization: Bearer TOKEN` |

---

## 📦 Dependencies

- fastapi - Web framework
- sqlalchemy - ORM
- pydantic - Validation
- python-jose - JWT
- passlib + bcrypt - Password security
- uvicorn - ASGI server

Full list: `requirements.txt`

---

## 📝 Status

✅ **Production Ready**
- Enterprise architecture
- Full authentication
- Complete API
- Test structure
- Professional logging
- Comprehensive docs

**Version:** 1.0.0  
**Updated:** February 2026

---

## 📖 Documentation Files

- **README.md** ← You are here
- **COMPLETE_GUIDE.md** - Comprehensive guide
- **ARCHITECTURE.md** - Architecture details
- **STRUCTURE.md** - Folder structure
- **API Docs** - http://localhost:8000/docs

---

## 🤝 Support

📧 Check documentation  
🐛 Review error logs in `logs/`  
🔍 See API docs at http://localhost:8000/docs  

---

*Production-ready Task Manager API with enterprise architecture patterns. Built with FastAPI, SQLAlchemy, and JWT authentication.*
- **sqlalchemy**: SQL toolkit and ORM
- **aiosqlite**: Async SQLite driver
- **python-jose[cryptography]**: JWT token management
- **passlib[bcrypt]**: Password hashing
- **python-multipart**: Form data handling
- **pydantic-settings**: Environment variable management

## License

This project is provided as-is for educational purposes.

## Support

For issues and questions, refer to the official FastAPI documentation:
- https://fastapi.tiangolo.com/
- https://docs.sqlalchemy.org/

## Version History

### v1.0.0 (2026-02-01)
- Initial release
- User authentication with JWT
- CRUD operations for tasks
- SQLite database integration
