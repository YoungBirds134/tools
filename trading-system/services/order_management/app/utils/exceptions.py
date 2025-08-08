"""
Custom exceptions for the trading system
"""

from typing import Optional, Dict, Any


class TradingSystemError(Exception):
    """Base exception for trading system"""
    
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        self.message = message
        self.error_code = error_code or "TRADING_SYSTEM_ERROR"
        self.details = details or {}
        super().__init__(self.message)


class SSIAPIError(TradingSystemError):
    """SSI API related errors"""
    
    def __init__(self, message: str, error_code: str = "SSI_API_ERROR", details: Dict[str, Any] = None):
        super().__init__(message, error_code, details)


class SSIAuthenticationError(SSIAPIError):
    """SSI authentication errors"""
    
    def __init__(self, message: str, error_code: str = "SSI_AUTH_ERROR", details: Dict[str, Any] = None):
        super().__init__(message, error_code, details)


class SSIRateLimitError(SSIAPIError):
    """SSI rate limit errors"""
    
    def __init__(self, message: str, error_code: str = "SSI_RATE_LIMIT_ERROR", details: Dict[str, Any] = None):
        super().__init__(message, error_code, details)


class SSINetworkError(SSIAPIError):
    """SSI network errors"""
    
    def __init__(self, message: str, error_code: str = "SSI_NETWORK_ERROR", details: Dict[str, Any] = None):
        super().__init__(message, error_code, details)


class ValidationError(TradingSystemError):
    """Data validation errors"""
    
    def __init__(self, message: str, field: str = None, error_code: str = "VALIDATION_ERROR", details: Dict[str, Any] = None):
        self.field = field
        super().__init__(message, error_code, details)


class OrderError(TradingSystemError):
    """Order related errors"""
    
    def __init__(self, message: str, order_id: str = None, error_code: str = "ORDER_ERROR", details: Dict[str, Any] = None):
        self.order_id = order_id
        super().__init__(message, error_code, details)


class TradingSessionError(TradingSystemError):
    """Trading session related errors"""
    
    def __init__(self, message: str, session: str = None, error_code: str = "TRADING_SESSION_ERROR", details: Dict[str, Any] = None):
        self.session = session
        super().__init__(message, error_code, details)


class RiskManagementError(TradingSystemError):
    """Risk management related errors"""
    
    def __init__(self, message: str, risk_type: str = None, error_code: str = "RISK_MANAGEMENT_ERROR", details: Dict[str, Any] = None):
        self.risk_type = risk_type
        super().__init__(message, error_code, details)


class ConfigurationError(TradingSystemError):
    """Configuration related errors"""
    
    def __init__(self, message: str, config_key: str = None, error_code: str = "CONFIGURATION_ERROR", details: Dict[str, Any] = None):
        self.config_key = config_key
        super().__init__(message, error_code, details)
