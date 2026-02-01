from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import settings

# Create database engine
if "sqlite" in settings.DATABASE_URL:
    # Use sync SQLite without aiosqlite for startup
    engine = create_engine(
        settings.DATABASE_URL.replace("sqlite+aiosqlite", "sqlite"),
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

# Create SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

