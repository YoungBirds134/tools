"""
Common base schemas for SSI Integration Service
"""
from typing import Any, Dict, Optional, List, Union
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class BaseResponse(BaseModel):
    """Base response model"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="forbid"
    )
    
    message: str = Field(..., description="Response message")
    status: Union[int, str] = Field(..., description="Response status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


class PaginatedRequest(BaseModel):
    """Base paginated request"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )
    
    page_index: int = Field(default=1, ge=1, le=10, description="Page index (1-10)")
    page_size: int = Field(default=10, ge=10, le=1000, description="Page size (10, 20, 50, 100, 1000)")
    ascending: Optional[bool] = Field(default=None, description="Sort order")


class DateRangeRequest(BaseModel):
    """Base date range request"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )
    
    from_date: str = Field(..., description="Start date (dd/mm/yyyy)")
    to_date: str = Field(..., description="End date (dd/mm/yyyy)")


class Market(str, Enum):
    """Market enumeration"""
    HOSE = "HOSE"
    HNX = "HNX"
    UPCOM = "UPCOM"
    DERIVATIVE = "DERIVATIVE"
    DER = "DER"
    BOND = "BOND"
    VN = "VN"  # For trading
    VNFE = "VNFE"  # For derivatives trading


class TradingSession(str, Enum):
    """Trading session enumeration"""
    ATO = "ATO"  # Opening Call Auction
    LO = "LO"   # Continuous Trading
    ATC = "ATC"  # Closing All Auction
    PT = "PT"   # Putthrough
    C = "C"     # Market Close
    BREAK = "BREAK"  # Lunch Break
    HALT = "HALT"    # Market Halt


class TradingStatus(str, Enum):
    """Trading status enumeration"""
    N = "N"    # Normal
    D = "D"    # Delisted
    H = "H"    # Halt
    S = "S"    # Suspend
    NL = "NL"  # New List
    ND = "ND"  # Sắp hủy niêm yết
    ST = "ST"  # Special Trading
    SA = "SA"  # Suspend A
    SP = "SP"  # Suspend PT


class OrderStatus(str, Enum):
    """Order status enumeration"""
    WA = "WA"     # Waiting Approval
    RS = "RS"     # Ready to Send Exch
    SD = "SD"     # Sent to Exch
    QU = "Qu"     # Queue in Exch
    FF = "FF"     # Fully Filled
    PF = "PF"     # Partially Filled
    FFPC = "FFPC" # Fully Filled Partially Cancelled
    WM = "WM"     # Waiting Modify
    WC = "WC"     # Waiting Cancel
    CL = "CL"     # Cancelled
    RJ = "RJ"     # Rejected
    EX = "EX"     # Expired
    SOR = "SOR"   # Stop Order Ready
    SOS = "SOS"   # Stop Order Sent
    IAV = "IAV"   # Pre-Session Order
    SOI = "SOI"   # Pre-Session Stop Order


class BuySell(str, Enum):
    """Buy/Sell enumeration"""
    B = "B"  # Buy
    S = "S"  # Sell


class OrderType(str, Enum):
    """Order type enumeration"""
    LO = "LO"  # Limit Order
    MP = "MP"  # Market Price
    ATO = "ATO"  # At the Opening
    ATC = "ATC"  # At the Close
    MOK = "MOK"  # Market or Cancel
    MAK = "MAK"  # Market at Kill
    PLO = "PLO"  # Post Limit Order


class TwoFactorType(int, Enum):
    """Two factor authentication type"""
    PIN = 0
    OTP = 1


class ErrorResponse(BaseModel):
    """Error response model"""
    model_config = ConfigDict(extra="forbid")
    
    message: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")


class SuccessResponse(BaseResponse):
    """Success response model"""
    data: Optional[Any] = Field(None, description="Response data")
    total_record: Optional[int] = Field(None, description="Total records")


class HealthCheckResponse(BaseModel):
    """Health check response"""
    model_config = ConfigDict(extra="forbid")
    
    status: str = Field("healthy", description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Check timestamp")
    version: str = Field(..., description="Service version")
    services: Dict[str, str] = Field(..., description="Dependent services status")
