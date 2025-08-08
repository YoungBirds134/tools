"""
Common database models and utilities.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Column, DateTime, String, Text, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from .config import get_settings


@as_declarative()
class BaseModel:
    """Base model with common fields."""
    
    id: Any
    __name__: str
    
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )
    created_by = Column(String(255), nullable=True)
    updated_by = Column(String(255), nullable=True)
    metadata_info = Column(Text, nullable=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"


class DatabaseManager:
    """Database connection and session manager."""
    
    def __init__(self, database_url: Optional[str] = None):
        """Initialize database manager."""
        settings = get_settings()
        self.database_url = database_url or settings.database.database_url
        
        self.engine = create_engine(
            self.database_url,
            echo=settings.database.echo_sql,
            pool_size=settings.database.pool_size,
            max_overflow=settings.database.max_overflow,
            pool_recycle=settings.database.pool_recycle,
            poolclass=QueuePool,
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
    
    def get_session(self):
        """Get database session."""
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()
    
    def create_tables(self):
        """Create all tables."""
        BaseModel.metadata.create_all(bind=self.engine)
    
    def drop_tables(self):
        """Drop all tables."""
        BaseModel.metadata.drop_all(bind=self.engine)


# Global database manager instance
db_manager = DatabaseManager()

# Dependency for FastAPI
def get_db():
    """FastAPI dependency for database session."""
    return db_manager.get_session()
