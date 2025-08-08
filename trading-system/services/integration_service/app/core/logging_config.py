"""
Logging configuration for SSI Integration Service
"""
import logging
import sys
from typing import Any, Dict
import structlog
from rich.logging import RichHandler
from config import settings


def setup_logging() -> None:
    """Configure structured logging"""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if settings.log_format == "json" 
            else structlog.dev.ConsoleRenderer(colors=True),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    if settings.log_format == "json":
        logging.basicConfig(
            format="%(message)s",
            stream=sys.stdout,
            level=getattr(logging, settings.log_level.upper()),
        )
    else:
        logging.basicConfig(
            format="%(message)s",
            level=getattr(logging, settings.log_level.upper()),
            handlers=[RichHandler()],
        )
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("aioredis").setLevel(logging.WARNING)


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance"""
    return structlog.get_logger(name)


class LoggerMixin:
    """Mixin to add logging capabilities to classes"""
    
    @property
    def logger(self) -> structlog.stdlib.BoundLogger:
        """Get logger for this class"""
        return get_logger(self.__class__.__name__)
    
    def log_info(self, message: str, **kwargs: Any) -> None:
        """Log info message with context"""
        self.logger.info(message, **kwargs)
    
    def log_warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message with context"""
        self.logger.warning(message, **kwargs)
    
    def log_error(self, message: str, **kwargs: Any) -> None:
        """Log error message with context"""
        self.logger.error(message, **kwargs)
    
    def log_debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message with context"""
        self.logger.debug(message, **kwargs)
