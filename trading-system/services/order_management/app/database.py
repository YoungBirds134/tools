"""
Database configuration and session management for Order Management Service.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

try:
    from ...common.config import get_config
    from ...common.logging import LoggerManager
except ImportError:
    # Fallback for development environment
    class MockConfig:
        DATABASE_URL = "sqlite:///./order_management.db"
        DATABASE_ECHO = False
    
    def get_config():
        return MockConfig()
    
    class MockLogger:
        def info(self, msg): print(f"INFO: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")
        def warning(self, msg): print(f"WARNING: {msg}")
    
    class MockLoggerManager:
        @staticmethod
        def get_logger(name): return MockLogger()
    
    LoggerManager = MockLoggerManager()

# Get configuration
config = get_config()
logger = LoggerManager.get_logger("database")

# Database URL
DATABASE_URL = getattr(config, 'DATABASE_URL', "sqlite:///./order_management.db")

# Create engine
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=getattr(config, 'DATABASE_ECHO', False)
    )
else:
    # PostgreSQL configuration
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=getattr(config, 'DATABASE_ECHO', False)
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()


def get_db() -> Session:
    """
    Dependency that provides a database session.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def init_database():
    """
    Initialize database tables.
    """
    try:
        # Import all models to ensure they are registered with Base
        from .models import (
            Order, OrderExecution, Position, PositionHistory
        )
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise


def drop_database():
    """
    Drop all database tables (for testing purposes).
    """
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
        
    except Exception as e:
        logger.error(f"Error dropping database: {str(e)}")
        raise


def reset_database():
    """
    Reset database by dropping and recreating all tables.
    """
    try:
        drop_database()
        init_database()
        logger.info("Database reset successfully")
        
    except Exception as e:
        logger.error(f"Error resetting database: {str(e)}")
        raise


def get_engine():
    """
    Get the database engine.
    """
    return engine


def check_database_connection():
    """
    Check if database connection is working.
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        logger.info("Database connection check successful")
        return True
        
    except Exception as e:
        logger.error(f"Database connection check failed: {str(e)}")
        return False


# Health check function for FastAPI
async def database_health_check():
    """
    Async health check for database connection.
    """
    try:
        db = SessionLocal()
        try:
            # Simple query to check connection
            db.execute("SELECT 1")
            return {"status": "healthy", "database": "connected"}
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


# Migration utilities
def get_alembic_config():
    """
    Get Alembic configuration for database migrations.
    """
    from alembic.config import Config
    from alembic import command
    
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    alembic_dir = os.path.join(current_dir, '..', 'alembic')
    alembic_ini = os.path.join(alembic_dir, 'alembic.ini')
    
    if os.path.exists(alembic_ini):
        alembic_cfg = Config(alembic_ini)
        alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
        return alembic_cfg
    else:
        logger.warning("Alembic configuration not found")
        return None


def run_migrations():
    """
    Run database migrations using Alembic.
    """
    try:
        from alembic import command
        
        alembic_cfg = get_alembic_config()
        if alembic_cfg:
            command.upgrade(alembic_cfg, "head")
            logger.info("Database migrations completed successfully")
        else:
            logger.warning("Skipping migrations - Alembic not configured")
            
    except ImportError:
        logger.warning("Alembic not installed - skipping migrations")
    except Exception as e:
        logger.error(f"Error running migrations: {str(e)}")
        raise


# Context manager for database transactions
class DatabaseTransaction:
    """
    Context manager for database transactions.
    """
    
    def __init__(self):
        self.db = None
    
    def __enter__(self) -> Session:
        self.db = SessionLocal()
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.db.rollback()
            logger.error(f"Transaction rolled back due to error: {exc_val}")
        else:
            self.db.commit()
        
        self.db.close()


# Utility function for executing raw SQL
def execute_raw_sql(sql: str, params: dict = None):
    """
    Execute raw SQL query.
    """
    try:
        with DatabaseTransaction() as db:
            result = db.execute(sql, params or {})
            return result.fetchall()
            
    except Exception as e:
        logger.error(f"Error executing raw SQL: {str(e)}")
        raise


# Database backup utilities (for SQLite)
def backup_database(backup_path: str):
    """
    Create a backup of the database (SQLite only).
    """
    if not DATABASE_URL.startswith("sqlite"):
        logger.warning("Database backup only supported for SQLite")
        return False
    
    try:
        import shutil
        
        # Extract database file path from URL
        db_file = DATABASE_URL.replace("sqlite:///", "")
        
        if os.path.exists(db_file):
            shutil.copy2(db_file, backup_path)
            logger.info(f"Database backed up to {backup_path}")
            return True
        else:
            logger.error(f"Database file not found: {db_file}")
            return False
            
    except Exception as e:
        logger.error(f"Error backing up database: {str(e)}")
        return False


def restore_database(backup_path: str):
    """
    Restore database from backup (SQLite only).
    """
    if not DATABASE_URL.startswith("sqlite"):
        logger.warning("Database restore only supported for SQLite")
        return False
    
    try:
        import shutil
        
        # Extract database file path from URL
        db_file = DATABASE_URL.replace("sqlite:///", "")
        
        if os.path.exists(backup_path):
            # Close all connections
            engine.dispose()
            
            # Restore backup
            shutil.copy2(backup_path, db_file)
            logger.info(f"Database restored from {backup_path}")
            return True
        else:
            logger.error(f"Backup file not found: {backup_path}")
            return False
            
    except Exception as e:
        logger.error(f"Error restoring database: {str(e)}")
        return False
