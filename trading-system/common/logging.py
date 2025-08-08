"""
Common logging utilities and configuration.
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional

from loguru import logger

from .config import get_settings


class LoggerManager:
    """Centralized logging manager for all microservices."""
    
    def __init__(self, service_name: str = "trading-system"):
        """Initialize logger manager."""
        self.service_name = service_name
        self.settings = get_settings().logging
        self._configure_logger()
    
    def _configure_logger(self):
        """Configure loguru logger."""
        # Remove default handler
        logger.remove()
        
        # Console handler
        logger.add(
            sys.stdout,
            format=self.settings.format,
            level=self.settings.level,
            colorize=True,
            serialize=False,
        )
        
        # File handler (if specified)
        if self.settings.file_path:
            log_file = Path(self.settings.file_path)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            logger.add(
                log_file,
                format=self.settings.format,
                level=self.settings.level,
                rotation=self.settings.max_file_size,
                retention=self.settings.retention,
                compression="zip",
                serialize=True,  # JSON format for file logs
            )
    
    def get_logger(self, name: Optional[str] = None) -> Any:
        """Get logger instance with service context."""
        context_name = f"{self.service_name}.{name}" if name else self.service_name
        return logger.bind(service=self.service_name, component=context_name)
    
    def bind_request_id(self, request_id: str) -> Any:
        """Bind request ID to logger context."""
        return logger.bind(request_id=request_id)
    
    def bind_user_id(self, user_id: str) -> Any:
        """Bind user ID to logger context."""
        return logger.bind(user_id=user_id)
    
    def log_api_request(
        self, 
        method: str, 
        path: str, 
        status_code: int, 
        duration: float,
        **kwargs: Any
    ):
        """Log API request with standardized format."""
        logger.info(
            "API Request",
            method=method,
            path=path,
            status_code=status_code,
            duration_ms=round(duration * 1000, 2),
            **kwargs
        )
    
    def log_database_query(self, query: str, duration: float, **kwargs: Any):
        """Log database query with performance metrics."""
        logger.debug(
            "Database Query",
            query=query,
            duration_ms=round(duration * 1000, 2),
            **kwargs
        )
    
    def log_external_api_call(
        self, 
        service: str, 
        endpoint: str, 
        method: str,
        status_code: int, 
        duration: float,
        **kwargs: Any
    ):
        """Log external API calls."""
        logger.info(
            "External API Call",
            service=service,
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            duration_ms=round(duration * 1000, 2),
            **kwargs
        )
    
    def log_business_event(self, event_type: str, event_data: Dict[str, Any]):
        """Log important business events."""
        logger.info(
            "Business Event",
            event_type=event_type,
            event_data=event_data
        )
    
    def log_error(self, error: Exception, context: Optional[Dict[str, Any]] = None):
        """Log errors with full context."""
        logger.error(
            f"Error: {str(error)}",
            error_type=type(error).__name__,
            context=context or {},
            exc_info=True
        )
    
    def log_security_event(self, event_type: str, user_id: Optional[str] = None, **kwargs: Any):
        """Log security-related events."""
        logger.warning(
            "Security Event",
            event_type=event_type,
            user_id=user_id,
            **kwargs
        )


# Global logger manager instance
logger_manager = LoggerManager()

# Convenience function to get logger
def get_logger(name: Optional[str] = None) -> Any:
    """Get logger instance."""
    return logger_manager.get_logger(name)
