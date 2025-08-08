"""
Order Management Service - Core trading operations with SSI FastConnect integration.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator
from sqlalchemy import (
    Column, String, Float, Integer, DateTime, Text, Enum as SQLEnum, 
    Boolean, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class OrderSide(str, Enum):
    """Order side enumeration."""
    BUY = "B"
    SELL = "S"


class OrderType(str, Enum):
    """Order type enumeration."""
    LIMIT = "LO"              # Limit Order
    MARKET_TO_LIMIT = "MTL"   # Market to Limit
    MATCH_OR_KILL = "MOK"     # Match or Kill
    MATCH_AND_KILL = "MAK"    # Match and Kill
    AT_THE_CLOSE = "ATC"      # At the Close
    AT_THE_OPEN = "ATO"       # At the Open
    POST_LIMIT = "PLO"        # Post Limit Order


class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "PENDING"
    SENT = "SENT"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class Market(str, Enum):
    """Market enumeration."""
    HOSE = "HOSE"
    HNX = "HNX"
    UPCOM = "UPCOM"


class TradingSession(str, Enum):
    """Trading session enumeration."""
    PRE_MARKET = "PRE_MARKET"
    MORNING_AUCTION = "MORNING_AUCTION"
    CONTINUOUS_MORNING = "CONTINUOUS_MORNING"
    LUNCH_BREAK = "LUNCH_BREAK"
    CONTINUOUS_AFTERNOON = "CONTINUOUS_AFTERNOON"
    CLOSING_AUCTION = "CLOSING_AUCTION"
    POST_MARKET = "POST_MARKET"
    CLOSED = "CLOSED"


# Legacy enums for backward compatibility
class BuySellEnum(str, Enum):
    """Buy/Sell direction enum - Legacy"""
    BUY = "B"
    SELL = "S"


class MarketEnum(str, Enum):
    """Market enum for Vietnamese exchanges - Legacy"""
    HOSE = "VN"  # Ho Chi Minh Stock Exchange
    HNX = "HN"   # Hanoi Stock Exchange
    UPCOM = "UP" # Unlisted Public Company Market
    DERIVATIVE = "VNFE"  # VN Futures Exchange


class OrderTypeEnum(str, Enum):
    """Order type enum according to HOSE and HNX regulations - Legacy"""
    # Common order types
    LIMIT = "LO"          # Limit Order
    MARKET_TO_LIMIT = "MTL"  # Market to Limit
    
    # HOSE specific
    ATO = "ATO"           # At the Open
    ATC = "ATC"           # At the Close
    
    # HNX specific  
    MATCH_OR_KILL = "MOK"  # Match or Kill
    MATCH_AND_KILL = "MAK" # Match and Kill
    POST_LIMIT = "PLO"     # Post Limit Order (after hours)


class TwoFATypeEnum(int, Enum):
    """Two-factor authentication type"""
    PIN = 0
    OTP = 1


class OrderStatusEnum(str, Enum):
    """Order status lifecycle"""
    PENDING = "PENDING"
    OPEN = "OPEN"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class TradingSessionEnum(str, Enum):
    """Trading session periods"""
    OPENING_AUCTION = "OPENING_AUCTION"      # 9:00-9:15 (HOSE)
    CONTINUOUS_1 = "CONTINUOUS_1"           # 9:15-11:30
    LUNCH_BREAK = "LUNCH_BREAK"             # 11:30-13:00
    CONTINUOUS_2 = "CONTINUOUS_2"           # 13:00-14:30
    CLOSING_AUCTION = "CLOSING_AUCTION"     # 14:30-14:45
    AFTER_HOURS = "AFTER_HOURS"             # 14:45-15:00
    PUT_THROUGH = "PUT_THROUGH"             # Block trading session


# Request Models with enhanced validation
class NewOrderRequest(BaseModel):
    """New order request according to SSI FastConnect specification"""
    instrument_id: str = Field(..., description="Security symbol", example="VCB")
    market: MarketEnum = Field(..., description="Market identifier")
    buy_sell: BuySellEnum = Field(..., description="Buy or Sell direction")
    order_type: OrderTypeEnum = Field(..., description="Order type")
    price: float = Field(..., ge=0, description="Order price")
    quantity: int = Field(..., gt=0, description="Order quantity")
    account: str = Field(..., description="Trading account")
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique request ID")
    
    # Optional fields for advanced orders
    stop_order: bool = Field(default=False, description="Is stop order")
    stop_price: float = Field(default=0, ge=0, description="Stop price")
    stop_type: str = Field(default="", description="Stop type")
    stop_step: float = Field(default=0, ge=0, description="Stop step")
    loss_step: float = Field(default=0, ge=0, description="Loss step")
    profit_step: float = Field(default=0, ge=0, description="Profit step")
    
    # Device and session tracking
    device_id: Optional[str] = Field(None, description="Device identifier")
    user_agent: Optional[str] = Field(None, description="User agent string")

    @validator('price')
    def validate_price(cls, v, values):
        """Validate price based on order type"""
        order_type = values.get('order_type')
        if order_type in [OrderTypeEnum.ATO, OrderTypeEnum.ATC] and v > 0:
            raise ValueError("ATO/ATC orders should have price = 0")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "instrument_id": "VCB",
                "market": "VN",
                "buy_sell": "B",
                "order_type": "LO",
                "price": 95000,
                "quantity": 100,
                "account": "0001234567",
                "request_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class ModifyOrderRequest(BaseModel):
    """Modify existing order request"""
    order_id: str = Field(..., description="Order ID to modify")
    instrument_id: str = Field(..., description="Security symbol")
    market: MarketEnum = Field(..., description="Market identifier")
    buy_sell: BuySellEnum = Field(..., description="Buy or Sell direction")
    order_type: OrderTypeEnum = Field(..., description="Order type")
    price: float = Field(..., ge=0, description="New order price")
    quantity: int = Field(..., gt=0, description="New order quantity")
    account: str = Field(..., description="Trading account")
    
    device_id: Optional[str] = Field(None, description="Device identifier")
    user_agent: Optional[str] = Field(None, description="User agent string")

    class Config:
        json_schema_extra = {
            "example": {
                "order_id": "ORD123456789",
                "instrument_id": "VCB",
                "market": "VN",
                "buy_sell": "B",
                "order_type": "LO",
                "price": 96000,
                "quantity": 200,
                "account": "0001234567"
            }
        }


class CancelOrderRequest(BaseModel):
    """Cancel order request"""
    order_id: str = Field(..., description="Order ID to cancel")
    instrument_id: str = Field(..., description="Security symbol")
    market: MarketEnum = Field(..., description="Market identifier")
    buy_sell: BuySellEnum = Field(..., description="Buy or Sell direction")
    account: str = Field(..., description="Trading account")
    
    device_id: Optional[str] = Field(None, description="Device identifier")
    user_agent: Optional[str] = Field(None, description="User agent string")

    class Config:
        json_schema_extra = {
            "example": {
                "order_id": "ORD123456789",
                "instrument_id": "VCB",
                "market": "VN",
                "buy_sell": "B",
                "account": "0001234567"
            }
        }

class AccountBalanceRequest(BaseModel):
    """Account balance query request"""
    account: str = Field(..., description="Trading account")

    class Config:
        json_schema_extra = {
            "example": {
                "account": "0001234567"
            }
        }


class PositionRequest(BaseModel):
    """Portfolio position query request"""
    account: str = Field(..., description="Trading account")
    query_summary: bool = Field(default=True, description="Include summary information")

    class Config:
        json_schema_extra = {
            "example": {
                "account": "0001234567",
                "query_summary": True
            }
        }


class MaxQuantityRequest(BaseModel):
    """Maximum tradeable quantity request"""
    account: str = Field(..., description="Trading account")
    instrument_id: str = Field(..., description="Security symbol")
    price: float = Field(default=0, ge=0, description="Order price (0 for market price)")

    class Config:
        json_schema_extra = {
            "example": {
                "account": "0001234567",
                "instrument_id": "VCB",
                "price": 95000
            }
        }


class OrderHistoryRequest(BaseModel):
    """Order history query request"""
    account: str = Field(..., description="Trading account")
    start_date: str = Field(..., description="Start date in DD/MM/YYYY format")
    end_date: str = Field(..., description="End date in DD/MM/YYYY format")

    @validator('start_date', 'end_date')
    def validate_date_format(cls, v):
        """Validate date format DD/MM/YYYY"""
        try:
            datetime.strptime(v, '%d/%m/%Y')
        except ValueError:
            raise ValueError('Date must be in DD/MM/YYYY format')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "account": "0001234567",
                "start_date": "01/01/2024",
                "end_date": "31/12/2024"
            }
        }


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


# Response Models
class APIResponse(BaseModel):
    """Base API response model"""
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
                "data": None,
                "error": None,
                "timestamp": "2024-01-01T12:00:00"
            }
        }


class OrderResponse(APIResponse):
    """Order operation response"""
    order_id: Optional[str] = Field(None, description="Generated order ID")
    request_id: Optional[str] = Field(None, description="Original request ID")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Order placed successfully",
                "data": {
                    "order_id": "ORD123456789",
                    "status": "PENDING"
                },
                "order_id": "ORD123456789",
                "request_id": "550e8400-e29b-41d4-a716-446655440000",
                "timestamp": "2024-01-01T12:00:00"
            }
        }


class BalanceResponse(APIResponse):
    """Account balance response"""
    account: str = Field(..., description="Trading account")
    balance: Optional[float] = Field(None, description="Available balance")
    currency: str = Field(default="VND", description="Currency code")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Balance retrieved successfully",
                "account": "0001234567",
                "balance": 1000000000.0,
                "currency": "VND",
                "timestamp": "2024-01-01T12:00:00"
            }
        }


class PositionResponse(APIResponse):
    """Portfolio position response"""
    account: str = Field(..., description="Trading account")
    positions: Optional[List[Dict[str, Any]]] = Field(None, description="Position details")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Positions retrieved successfully",
                "account": "0001234567",
                "positions": [
                    {
                        "instrument_id": "VCB",
                        "quantity": 1000,
                        "average_price": 94500,
                        "market_value": 94500000,
                        "unrealized_pnl": 500000
                    }
                ],
                "timestamp": "2024-01-01T12:00:00"
            }
        }


class OrderBookResponse(APIResponse):
    """Order book/history response"""
    account: str = Field(..., description="Trading account")
    orders: Optional[List[Dict[str, Any]]] = Field(None, description="Order details")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Orders retrieved successfully",
                "account": "0001234567",
                "orders": [
                    {
                        "order_id": "ORD123456789",
                        "instrument_id": "VCB",
                        "order_type": "LO",
                        "buy_sell": "B",
                        "price": 95000,
                        "quantity": 100,
                        "filled_quantity": 0,
                        "status": "OPEN",
                        "order_time": "2024-01-01T09:15:00"
                    }
                ],
                "timestamp": "2024-01-01T12:00:00"
            }
        }


class MaxQuantityResponse(APIResponse):
    """Maximum quantity response"""
    account: str = Field(..., description="Trading account")
    instrument_id: str = Field(..., description="Security symbol")
    max_buy_quantity: Optional[int] = Field(None, description="Maximum buyable quantity")
    max_sell_quantity: Optional[int] = Field(None, description="Maximum sellable quantity")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Max quantities calculated successfully",
                "account": "0001234567",
                "instrument_id": "VCB",
                "max_buy_quantity": 1052,
                "max_sell_quantity": 1000,
                "timestamp": "2024-01-01T12:00:00"
            }
        }


# Trading session validation models
class TradingSession(BaseModel):
    """Trading session information"""
    session: TradingSessionEnum
    start_time: str = Field(..., description="Session start time (HH:MM)")
    end_time: str = Field(..., description="Session end time (HH:MM)")
    allowed_order_types: List[OrderTypeEnum] = Field(..., description="Allowed order types")
    can_cancel: bool = Field(..., description="Can cancel orders in this session")
    can_modify: bool = Field(..., description="Can modify orders in this session")

    class Config:
        json_schema_extra = {
            "example": {
                "session": "CONTINUOUS_1",
                "start_time": "09:15",
                "end_time": "11:30",
                "allowed_order_types": ["LO", "MTL"],
                "can_cancel": True,
                "can_modify": True
            }
        }


# Market data models for internal use
class SecurityInfo(BaseModel):
    """Security master data"""
    instrument_id: str = Field(..., description="Security symbol")
    instrument_name: str = Field(..., description="Security name")
    market: MarketEnum = Field(..., description="Market")
    lot_size: int = Field(..., description="Lot size")
    tick_size: float = Field(..., description="Minimum price increment")
    price_limit_up: Optional[float] = Field(None, description="Daily price limit up")
    price_limit_down: Optional[float] = Field(None, description="Daily price limit down")
    is_tradeable: bool = Field(default=True, description="Is currently tradeable")

    class Config:
        json_schema_extra = {
            "example": {
                "instrument_id": "VCB",
                "instrument_name": "Joint Stock Commercial Bank for Foreign Trade of Vietnam",
                "market": "VN",
                "lot_size": 100,
                "tick_size": 100,
                "price_limit_up": 101500,
                "price_limit_down": 88500,
                "is_tradeable": True
            }
        }


# Standard Response DTOs for internal API consistency
class StandardResponse(BaseModel):
    """Standard response format for internal APIs"""
    success: bool = Field(..., description="Operation success status", example=True)
    message: str = Field(..., description="Response message", example="Operation completed successfully")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": None
            }
        }

