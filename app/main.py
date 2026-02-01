import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add parent directory to path to enable imports from routers
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import Base, engine
from routers import auth, tasks

# Create FastAPI app
app = FastAPI(
    title="Task Manager API",
    description="A simple task manager API with user authentication",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
@app.on_event("startup")
def startup():
    """Create database tables on startup"""
    Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Task Manager API",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy"}
