from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Generator, Session
from app.core.config import settings


# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency used in FastAPI routes to get DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()