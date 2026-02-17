"""
Database Connection and Session Management
PostgreSQL database setup using SQLModel
"""

import os
from sqlmodel import Session, create_engine, SQLModel, text
from typing import Generator
from ..core import logger


# Get database URL from environment or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/medical_db"
)

# Create database engine
try:
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Set to True for SQL query logging
        pool_pre_ping=True,  # Verify connections before using
        pool_size=5,
        max_overflow=10
    )
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    engine = None


def init_db() -> None:
    """
    Initialize database tables
    Creates all tables defined in SQLModel models
    """
    if engine is None:
        logger.error("Cannot initialize database: engine not created")
        return
        
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    
    Yields:
        Session: SQLModel database session
        
    Usage:
        @app.get("/users")
        def get_users(session: Session = Depends(get_session)):
            ...
    """
    if engine is None:
        raise RuntimeError("Database engine not initialized")
        
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            session.rollback()
            raise
        finally:
            session.close()


def check_db_connection() -> bool:
    """
    Check if database connection is working
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    if engine is None:
        return False
        
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False
