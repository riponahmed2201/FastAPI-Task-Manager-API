# Task Manager API

A FastAPI-based task management application with user authentication using JWT tokens.

## Features

- User registration and login with secure password hashing
- JWT token-based authentication
- CRUD operations for tasks
- Task completion status tracking
- User-specific task management
- CORS enabled for cross-origin requests
- Interactive API documentation

## Project Structure

```
task-manager-app/
├── app/
│   ├── __init__.py           # App package
│   ├── main.py               # FastAPI application entry point
│   ├── models.py             # SQLAlchemy ORM models
│   ├── schemas.py            # Pydantic request/response schemas
│   ├── database.py           # Database configuration
│   ├── dependencies.py       # Dependency injection and authentication
│   └── crud.py               # CRUD operations
├── routers/
│   ├── __init__.py           # Routers package
│   ├── auth.py               # Authentication endpoints
│   └── tasks.py              # Task management endpoints
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── README.md                 # This file
```

## Installation

### Prerequisites

- Python 3.9+
- pip

### Setup

1. **Clone the repository** (if applicable)

2. **Create a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

Windows:
```bash
venv\Scripts\activate
```

Unix/macOS:
```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Configure environment variables**

Edit `.env` file and update if needed:
```
DATABASE_URL=sqlite:///./tasks.db
SECRET_KEY=your-super-secret-key-change-this-in-production-12345
```

## Running the Application

### Start the server

```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

### Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## API Endpoints

### Authentication

#### Register User
```
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword"
}

Response: 201
{
  "id": 1,
  "username": "john_doe"
}
```

#### Login
```
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=securepassword

Response: 200
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### Get Current User
```
GET /auth/me
Authorization: Bearer {token}

Response: 200
{
  "id": 1,
  "username": "john_doe"
}
```

### Tasks

#### Get All Tasks (for current user)
```
GET /tasks/
Authorization: Bearer {token}

Response: 200
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "owner_id": 1
  }
]
```

#### Create Task
```
POST /tasks/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Complete project",
  "description": "Finish the FastAPI task manager"
}

Response: 201
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the FastAPI task manager",
  "completed": false,
  "owner_id": 1
}
```

#### Update Task
```
PUT /tasks/{task_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Complete project",
  "description": "Updated description"
}

Response: 200
{
  "id": 1,
  "title": "Complete project",
  "description": "Updated description",
  "completed": false,
  "owner_id": 1
}
```

#### Mark Task Complete
```
PATCH /tasks/{task_id}/complete
Authorization: Bearer {token}

Response: 200
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the FastAPI task manager",
  "completed": true,
  "owner_id": 1
}
```

#### Mark Task Incomplete
```
PATCH /tasks/{task_id}/incomplete
Authorization: Bearer {token}

Response: 200
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the FastAPI task manager",
  "completed": false,
  "owner_id": 1
}
```

#### Delete Task
```
DELETE /tasks/{task_id}
Authorization: Bearer {token}

Response: 200
{
  "message": "Task deleted successfully"
}
```

### Health Check

```
GET /health

Response: 200
{
  "status": "healthy"
}
```

## Database

The application uses SQLite by default. The database file (`tasks.db`) is created automatically on first startup.

### Models

#### User
- `id`: Integer (primary key)
- `username`: String (unique)
- `hashed_password`: String
- `tasks`: Relationship to Task

#### Task
- `id`: Integer (primary key)
- `title`: String
- `description`: String (optional)
- `completed`: Boolean (default: False)
- `owner_id`: Integer (foreign key to User)
- `owner`: Relationship to User

## Authentication

The API uses JWT (JSON Web Token) for authentication:

1. **Register** a new user account
2. **Login** with credentials to receive an access token
3. **Include** the token in the `Authorization` header for protected endpoints:
   ```
   Authorization: Bearer {access_token}
   ```

Tokens expire after 30 minutes.

## Security Notes

⚠️ **Important for Production:**

1. Change the `SECRET_KEY` in `.env` to a strong, random value
2. Use environment variables for sensitive configuration
3. Enable HTTPS/TLS for all communications
4. Use a production database (PostgreSQL, MySQL) instead of SQLite
5. Implement rate limiting
6. Add input validation and sanitization
7. Enable CORS only for trusted origins
8. Use strong password requirements

## Development

### Running Tests

Create a `test_*.py` file and run:

```bash
pytest
```

### Code Style

The project follows PEP 8 style guidelines. Format code with:

```bash
black .
flake8 .
```

## Troubleshooting

### Port already in use

Change the port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Database locked error

Delete `tasks.db` and restart the application.

### Import errors

Ensure you're in the virtual environment and all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Dependencies

- **fastapi[all]**: FastAPI framework with all standard tools
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
