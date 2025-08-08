"""
Exception classes for SSI Integration Service
"""
from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class SSIIntegrationError(Exception):
    """Base exception for SSI Integration Service"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class SSIAPIError(SSIIntegrationError):
    """Exception for SSI API errors"""
    
    def __init__(
        self, 
        message: str, 
        status_code: int, 
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message, details)


class SSIAuthenticationError(SSIAPIError):
    """Exception for authentication errors"""
    
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, "AUTH_ERROR", details)


class SSIAuthorizationError(SSIAPIError):
    """Exception for authorization errors"""
    
    def __init__(self, message: str = "Authorization failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_403_FORBIDDEN, "AUTH_FORBIDDEN", details)


class SSIValidationError(SSIAPIError):
    """Exception for validation errors"""
    
    def __init__(self, message: str, field: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.field = field
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY, "VALIDATION_ERROR", details)


class SSIRateLimitError(SSIAPIError):
    """Exception for rate limit errors"""
    
    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_429_TOO_MANY_REQUESTS, "RATE_LIMIT", details)


class SSINetworkError(SSIIntegrationError):
    """Exception for network-related errors"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)


class SSICacheError(SSIIntegrationError):
    """Exception for cache-related errors"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)


class SSIConfigurationError(SSIIntegrationError):
    """Exception for configuration errors"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)


class SSIDataNotFoundError(SSIAPIError):
    """Exception for data not found errors"""
    
    def __init__(self, message: str = "Data not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, "DATA_NOT_FOUND", details)


class SSIServerError(SSIAPIError):
    """Exception for server errors"""
    
    def __init__(self, message: str = "Internal server error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, "SERVER_ERROR", details)


# HTTP Exception converters
def ssi_api_error_to_http_exception(error: SSIAPIError) -> HTTPException:
    """Convert SSI API error to FastAPI HTTPException"""
    return HTTPException(
        status_code=error.status_code,
        detail={
            "message": error.message,
            "error_code": error.error_code,
            "details": error.details
        }
    )


def ssi_integration_error_to_http_exception(error: SSIIntegrationError) -> HTTPException:
    """Convert SSI Integration error to FastAPI HTTPException"""
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "message": error.message,
            "error_code": "INTEGRATION_ERROR",
            "details": error.details
        }
    )
