"""
Pydantic models for Config Service
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class TwoFATypeEnum(int, Enum):
    """Two-factor authentication type"""
    PIN = 0
    OTP = 1


class ConfigTypeEnum(str, Enum):
    """Configuration value type"""
    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    JSON = "json"


class OTPRequest(BaseModel):
    """OTP request for 2FA authentication"""
    account: str = Field(..., description="Trading account")
    two_fa_type: TwoFATypeEnum = Field(default=TwoFATypeEnum.OTP, description="2FA type")
    
    class Config:
        json_schema_extra = {
            "example": {
                "account": "0001234567",
                "two_fa_type": 1
            }
        }


class VerifyCodeRequest(BaseModel):
    """Verification code for 2FA"""
    code: str = Field(..., description="OTP or PIN code")
    account: str = Field(..., description="Trading account")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "123456",
                "account": "0001234567"
            }
        }


class SSIResponse(BaseModel):
    """SSI API response model"""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error details if any")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {
                    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "expires_in": 3600
                },
                "timestamp": "2025-07-16T00:00:00Z"
            }
        }


class ConfigRequest(BaseModel):
    """Configuration set request"""
    key: str = Field(..., description="Configuration key")
    value: str = Field(..., description="Configuration value")
    config_type: ConfigTypeEnum = Field(default=ConfigTypeEnum.STRING, description="Configuration type")
    description: str = Field(default="", description="Configuration description")
    
    @validator('key')
    def validate_key(cls, v):
        """Validate configuration key"""
        if not v or not v.strip():
            raise ValueError("Configuration key cannot be empty")
        if len(v) > 100:
            raise ValueError("Configuration key too long")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "key": "SSI_CONSUMER_ID",
                "value": "your_consumer_id",
                "config_type": "string",
                "description": "SSI FastConnect Consumer ID"
            }
        }


class ConfigResponse(BaseModel):
    """Configuration response model"""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error details if any")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Configuration retrieved successfully",
                "data": {
                    "SSI_CONSUMER_ID": {
                        "value": "your_consumer_id",
                        "type": "string",
                        "description": "SSI FastConnect Consumer ID"
                    }
                },
                "timestamp": "2025-07-16T00:00:00Z"
            }
        }


class ConfigBatchRequest(BaseModel):
    """Batch configuration request"""
    keys: List[str] = Field(..., description="Configuration keys to retrieve")
    
    @validator('keys')
    def validate_keys(cls, v):
        """Validate configuration keys"""
        if not v:
            raise ValueError("Keys list cannot be empty")
        if len(v) > 100:
            raise ValueError("Too many keys requested")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "keys": ["SSI_CONSUMER_ID", "SSI_CONSUMER_SECRET", "DATABASE_URL"]
            }
        }


class ConfigBatchResponse(BaseModel):
    """Batch configuration response model"""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, str] = Field(default_factory=dict, description="Configuration values")
    missing_keys: List[str] = Field(default_factory=list, description="Keys not found")
    error: Optional[str] = Field(None, description="Error details if any")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Batch configuration retrieved successfully",
                "data": {
                    "SSI_CONSUMER_ID": "your_consumer_id",
                    "DATABASE_URL": "postgresql://user:pass@localhost:5432/db"
                },
                "missing_keys": ["SSI_CONSUMER_SECRET"],
                "timestamp": "2025-07-16T00:00:00Z"
            }
        }


class FeatureFlagsResponse(BaseModel):
    """Feature flags response model"""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, bool] = Field(default_factory=dict, description="Feature flags")
    error: Optional[str] = Field(None, description="Error details if any")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Feature flags retrieved successfully",
                "data": {
                    "ENABLE_TRADING": True,
                    "ENABLE_REAL_API": False,
                    "ENABLE_AUDIT_LOGGING": True,
                    "ENABLE_PERFORMANCE_LOGGING": True
                },
                "timestamp": "2025-07-16T00:00:00Z"
            }
        }


class CacheResponse(BaseModel):
    """Cache operation response model"""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Cache statistics")
    error: Optional[str] = Field(None, description="Error details if any")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Cache cleared successfully",
                "data": {
                    "cache_size": 0,
                    "redis_keys_deleted": 15
                },
                "timestamp": "2025-07-16T00:00:00Z"
            }
        }


class HealthResponse(BaseModel):
    """Health check response model"""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Health status")
    error: Optional[str] = Field(None, description="Error details if any")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Service is healthy",
                "data": {
                    "database": "healthy",
                    "redis": "healthy",
                    "ssi_service": "healthy",
                    "cache_size": 25
                },
                "timestamp": "2025-07-16T00:00:00Z"
            }
        } 