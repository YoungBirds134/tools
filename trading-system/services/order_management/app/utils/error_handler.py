"""
Error handling utilities for FC Trading API
"""
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


def handle_fc_trading_error(e: Exception, operation: str = "operation") -> None:
    """
    Handle FCTradingClient errors and raise appropriate HTTP exceptions
    
    Args:
        e: The exception to handle
        operation: Description of the operation that failed
    """
    error_message = str(e)
    
    # Handle FCTradingClient not initialized error
    if "FCTradingClient is not initialized" in error_message:
        raise HTTPException(
            status_code=503,
            detail="Trading service is not configured. Please check your PRIVATE_KEY configuration."
        )
    
    # Handle other ValueError types (usually configuration issues)
    if isinstance(e, ValueError):
        raise HTTPException(status_code=400, detail=error_message)
    
    # Handle connection errors
    if "connection" in error_message.lower() or "timeout" in error_message.lower():
        raise HTTPException(
            status_code=502,
            detail="Trading service is currently unavailable. Please try again later."
        )
    
    # Handle authentication errors
    if "authentication" in error_message.lower() or "unauthorized" in error_message.lower():
        raise HTTPException(
            status_code=401,
            detail="Authentication failed. Please check your credentials."
        )
    
    # Default to internal server error
    logger.error(f"Error in {operation}: {error_message}")
    raise HTTPException(status_code=500, detail=f"Internal server error: {error_message}")


def safe_service_call(service_func, operation: str = "operation"):
    """
    Safely call a service function and handle common errors
    
    Args:
        service_func: The service function to call
        operation: Description of the operation
    
    Returns:
        The result of the service function
    """
    try:
        return service_func()
    except Exception as e:
        handle_fc_trading_error(e, operation)
