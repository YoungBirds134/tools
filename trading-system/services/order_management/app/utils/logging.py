"""
Enhanced logging configuration using structlog for better structured logging
"""

import logging
import sys
import json
from pathlib import Path
from typing import Optional
import structlog
from datetime import datetime


def setup_logging(log_level: str = "INFO", log_format: str = None, use_json: bool = True):
    """
    Setup enhanced logging configuration with structlog
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_format: Custom log format (if not using structured logging)
        use_json: Whether to use JSON formatting for structured logs
    """
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure structlog
    structlog.configure(
        processors=[
            # Add timestamp and log level
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            
            # Add common context
            add_app_context,
            
            # JSON formatting for production, key-value for development
            structlog.processors.JSONRenderer() if use_json else structlog.dev.ConsoleRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    if log_format is None:
        if use_json:
            log_format = "%(message)s"  # structlog handles formatting
        else:
            log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # File handler for all logs
    file_handler = logging.FileHandler(log_dir / "app.log", mode='a', encoding='utf-8')
    file_handler.setLevel(getattr(logging, log_level.upper()))
    
    # Console handler for development
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[file_handler, console_handler],
        force=True
    )
    
    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("ssi_fctrading").setLevel(logging.DEBUG)
    
    # Application loggers
    logging.getLogger("app").setLevel(getattr(logging, log_level.upper()))
    
    logger = structlog.get_logger("app.logging")
    logger.info("Logging system initialized", 
                log_level=log_level, 
                json_format=use_json,
                log_dir=str(log_dir))


def add_app_context(logger, method_name, event_dict):
    """Add application context to log entries"""
    event_dict.update({
        "service": "order_management",
        "version": "1.0.0",
        "environment": "development"  # Should be from config
    })
    return event_dict


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get structured logger instance
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


class RequestLoggerMiddleware:
    """Middleware to add request context to logs"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Extract request info
            request_id = scope.get("headers", {}).get("x-request-id", "unknown")
            method = scope.get("method", "unknown")
            path = scope.get("path", "unknown")
            
            # Bind context to structlog
            structlog.contextvars.bind_contextvars(
                request_id=request_id,
                method=method,
                path=path
            )
        
        await self.app(scope, receive, send)


def log_function_call(func_name: str, **kwargs):
    """Decorator to log function calls with parameters"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            logger.info(f"Calling {func_name}", 
                       function=func_name,
                       args_count=len(args),
                       kwargs=kwargs)
            try:
                result = func(*args, **kwargs)
                logger.info(f"Completed {func_name}", 
                           function=func_name,
                           success=True)
                return result
            except Exception as e:
                logger.error(f"Error in {func_name}",
                           function=func_name,
                           error=str(e),
                           success=False)
                raise
        return wrapper
    return decorator


async def log_async_function_call(func_name: str, **kwargs):
    """Decorator to log async function calls with parameters"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            logger.info(f"Calling async {func_name}", 
                       function=func_name,
                       args_count=len(args),
                       kwargs=kwargs)
            try:
                result = await func(*args, **kwargs)
                logger.info(f"Completed async {func_name}", 
                           function=func_name,
                           success=True)
                return result
            except Exception as e:
                logger.error(f"Error in async {func_name}",
                           function=func_name,
                           error=str(e),
                           success=False)
                raise
        return wrapper
    return decorator


class PerformanceLogger:
    """Context manager for logging performance metrics"""
    
    def __init__(self, operation_name: str, logger: Optional[structlog.BoundLogger] = None):
        self.operation_name = operation_name
        self.logger = logger or get_logger("app.performance")
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info("Performance tracking started", 
                        operation=self.operation_name,
                        start_time=self.start_time.isoformat())
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        if exc_type is None:
            self.logger.info("Performance tracking completed",
                           operation=self.operation_name,
                           duration_seconds=duration,
                           success=True)
        else:
            self.logger.error("Performance tracking failed",
                            operation=self.operation_name,
                            duration_seconds=duration,
                            error=str(exc_val),
                            success=False)


# Security logging helpers
def log_security_event(event_type: str, details: dict, severity: str = "INFO"):
    """Log security-related events"""
    logger = get_logger("app.security")
    
    log_data = {
        "event_type": event_type,
        "severity": severity,
        "timestamp": datetime.now().isoformat(),
        **details
    }
    
    if severity.upper() == "ERROR":
        logger.error("Security event", **log_data)
    elif severity.upper() == "WARNING":
        logger.warning("Security event", **log_data)
    else:
        logger.info("Security event", **log_data)


def log_audit_event(action: str, resource: str, user: str = None, details: dict = None):
    """Log audit events for compliance"""
    logger = get_logger("app.audit")
    
    audit_data = {
        "action": action,
        "resource": resource,
        "user": user or "system",
        "timestamp": datetime.now().isoformat(),
        "details": details or {}
    }
    
    logger.info("Audit event", **audit_data)
