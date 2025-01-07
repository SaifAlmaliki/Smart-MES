"""
Database session dependency for FastAPI endpoints.
"""

from typing import Generator

def get_db() -> Generator:
    """
    Get a database session for dependency injection.
    Yields a SQLAlchemy session that is automatically closed after use.
    """
    from database.engine import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()