"""
Market Data Models for Vietnamese Stock Market
Enhanced data models for SSI FastConnect API and market data processing
"""

from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime, time
from datetime import date as Date
from decimal import Decimal
from enum import Enum


class MarketEnum(str, Enum):
    """Vietnamese stock exchanges"""
    HOSE = "HOSE"  # Ho Chi Minh Stock Exchange
    HNX = "HNX"    # Hanoi Stock Exchange  
    UPCOM = "UPCOM"  # Unlisted Public Company Market


class SessionEnum(str, Enum):
    """Trading sessions for Vietnamese market"""
    PRE_OPEN = "PRE_OPEN"      # 8:00-8:45 HOSE, 8:00-8:30 HNX
    CONTINUOUS = "CONTINUOUS"   # 9:00-11:30, 13:00-15:00 HOSE
    INTERMISSION = "INTERMISSION"  # 11:30-13:00
    CLOSE = "CLOSE"            # 15:00-15:15 closing auction
    POST_CLOSE = "POST_CLOSE"   # After 15:15
    AFTER_HOURS = "AFTER_HOURS"  # 15:30-16:30 for certain transactions


class DataTypeEnum(str, Enum):
    """Types of market data"""
    QUOTE = "QUOTE"          # Price quotes
    TRADE = "TRADE"          # Executed trades
    ORDER_BOOK = "ORDER_BOOK"  # Order book depth
    INDEX = "INDEX"          # Market indices
    NEWS = "NEWS"            # Market news
    ANNOUNCEMENT = "ANNOUNCEMENT"  # Corporate announcements


class PriceTypeEnum(str, Enum):
    """Price types in Vietnamese market"""
    CEILING = "CE"    # Ceiling price (tran tren)
    FLOOR = "FL"      # Floor price (tran duoi)
    REFERENCE = "REF"  # Reference price (gia tham chieu)
    MARKET = "MP"     # Market price
    LIMIT = "LO"      # Limit order price


# Base Models
class BaseMarketData(BaseModel):
    """Base class for all market data"""
    symbol: str = Field(..., description="Stock symbol")
    market: MarketEnum = Field(..., description="Exchange market")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Data timestamp")
    session: SessionEnum = Field(..., description="Trading session")
    
    @validator("symbol")
    def validate_symbol(cls, v):
        if not v or len(v) < 2 or len(v) > 10:
            raise ValueError("Symbol must be 2-10 characters")
        return v.upper()


class PriceData(BaseModel):
    """Price information"""
    price: Decimal = Field(..., ge=0, description="Price value")
    volume: int = Field(default=0, ge=0, description="Volume at this price")
    change: Optional[Decimal] = Field(None, description="Price change")
    change_percent: Optional[Decimal] = Field(None, description="Price change percentage")


class QuoteData(BaseMarketData):
    """Real-time quote data"""
    # Current prices
    last_price: Decimal = Field(..., ge=0, description="Last traded price")
    last_volume: int = Field(default=0, ge=0, description="Last traded volume")
    
    # Price levels
    ceiling_price: Decimal = Field(..., ge=0, description="Ceiling price")
    floor_price: Decimal = Field(..., ge=0, description="Floor price")
    reference_price: Decimal = Field(..., ge=0, description="Reference price")
    
    # Best bid/ask
    bid_price: Optional[Decimal] = Field(None, ge=0, description="Best bid price")
    bid_volume: Optional[int] = Field(None, ge=0, description="Best bid volume")
    ask_price: Optional[Decimal] = Field(None, ge=0, description="Best ask price")
    ask_volume: Optional[int] = Field(None, ge=0, description="Best ask volume")
    
    # Daily statistics
    open_price: Optional[Decimal] = Field(None, ge=0, description="Opening price")
    high_price: Optional[Decimal] = Field(None, ge=0, description="Highest price")
    low_price: Optional[Decimal] = Field(None, ge=0, description="Lowest price")
    
    # Volume and value
    total_volume: int = Field(default=0, ge=0, description="Total traded volume")
    total_value: Decimal = Field(default=0, ge=0, description="Total traded value")
    
    # Foreign trading
    foreign_buy_volume: Optional[int] = Field(None, ge=0, description="Foreign buy volume")
    foreign_sell_volume: Optional[int] = Field(None, ge=0, description="Foreign sell volume")
    
    # Additional fields
    lot_size: int = Field(default=100, ge=1, description="Lot size")
    
    @validator("ceiling_price", "floor_price", "reference_price")
    def validate_price_relationship(cls, v, values, field):
        if field.name == "ceiling_price" and "reference_price" in values:
            ref_price = values["reference_price"]
            if v < ref_price:
                raise ValueError("Ceiling price must be >= reference price")
        elif field.name == "floor_price" and "reference_price" in values:
            ref_price = values["reference_price"]
            if v > ref_price:
                raise ValueError("Floor price must be <= reference price")
        return v


class TradeData(BaseMarketData):
    """Individual trade data"""
    trade_id: str = Field(..., description="Unique trade identifier")
    price: Decimal = Field(..., ge=0, description="Trade price")
    volume: int = Field(..., ge=1, description="Trade volume")
    value: Decimal = Field(..., ge=0, description="Trade value")
    side: str = Field(..., description="Trade side (B/S)")
    trade_time: datetime = Field(..., description="Trade execution time")
    
    # Additional trade info
    match_type: Optional[str] = Field(None, description="Match type")
    is_foreign: Optional[bool] = Field(None, description="Is foreign trade")
    
    @validator("side")
    def validate_side(cls, v):
        if v not in ["B", "S", "BUY", "SELL"]:
            raise ValueError("Side must be B, S, BUY, or SELL")
        return v


class OrderBookLevel(BaseModel):
    """Single level of order book"""
    price: Decimal = Field(..., ge=0, description="Price level")
    volume: int = Field(..., ge=0, description="Volume at price level")
    orders: Optional[int] = Field(None, ge=0, description="Number of orders")


class OrderBookData(BaseMarketData):
    """Order book depth data"""
    # Bid side (buy orders)
    bids: List[OrderBookLevel] = Field(default_factory=list, description="Bid levels")
    
    # Ask side (sell orders)  
    asks: List[OrderBookLevel] = Field(default_factory=list, description="Ask levels")
    
    # Summary data
    total_bid_volume: int = Field(default=0, ge=0, description="Total bid volume")
    total_ask_volume: int = Field(default=0, ge=0, description="Total ask volume")
    spread: Optional[Decimal] = Field(None, ge=0, description="Bid-ask spread")
    
    @validator("bids", "asks")
    def validate_levels(cls, v):
        if len(v) > 10:  # Limit to top 10 levels
            return v[:10]
        return v


class IndexData(BaseModel):
    """Market index data"""
    index_code: str = Field(..., description="Index code (VN-Index, HNX-Index, etc.)")
    index_value: Decimal = Field(..., ge=0, description="Index value")
    change: Decimal = Field(..., description="Index change")
    change_percent: Decimal = Field(..., description="Index change percentage")
    volume: int = Field(default=0, ge=0, description="Total market volume")
    value: Decimal = Field(default=0, ge=0, description="Total market value")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Data timestamp")
    
    # Additional index metrics
    advances: Optional[int] = Field(None, ge=0, description="Number of advancing stocks")
    declines: Optional[int] = Field(None, ge=0, description="Number of declining stocks")
    unchanged: Optional[int] = Field(None, ge=0, description="Number of unchanged stocks")


class MarketNewsData(BaseModel):
    """Market news and announcements"""
    news_id: str = Field(..., description="Unique news identifier")
    title: str = Field(..., description="News title")
    content: Optional[str] = Field(None, description="News content")
    symbol: Optional[str] = Field(None, description="Related symbol")
    category: str = Field(..., description="News category")
    source: str = Field(..., description="News source")
    publish_time: datetime = Field(..., description="Publication time")
    importance: Optional[int] = Field(None, ge=1, le=5, description="Importance level 1-5")


# Request/Response Models
class SymbolListRequest(BaseModel):
    """Request for symbol list"""
    market: Optional[MarketEnum] = Field(None, description="Filter by market")
    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(default=100, ge=1, le=1000, description="Items per page")


class MarketDataRequest(BaseModel):
    """Request for market data"""
    symbols: List[str] = Field(..., min_items=1, max_items=50, description="List of symbols")
    data_types: List[DataTypeEnum] = Field(default=[DataTypeEnum.QUOTE], description="Data types requested")
    include_history: bool = Field(default=False, description="Include historical data")
    
    @validator("symbols")
    def validate_symbols(cls, v):
        return [symbol.upper() for symbol in v]


class MarketDataResponse(BaseModel):
    """Response with market data"""
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    data: Dict[str, Any] = Field(..., description="Market data by symbol")
    total_symbols: int = Field(..., ge=0, description="Total symbols in response")
    session_info: Optional[Dict[str, Any]] = Field(None, description="Current session information")


class StreamSubscriptionRequest(BaseModel):
    """Request to subscribe to real-time data"""
    symbols: List[str] = Field(..., min_items=1, max_items=100, description="Symbols to subscribe")
    data_types: List[DataTypeEnum] = Field(default=[DataTypeEnum.QUOTE], description="Data types to stream")
    
    @validator("symbols")
    def validate_symbols(cls, v):
        return [symbol.upper() for symbol in v]


class HistoricalDataRequest(BaseModel):
    """Request for historical data"""
    symbol: str = Field(..., description="Stock symbol")
    from_date: Date = Field(..., description="Start date")
    to_date: Date = Field(..., description="End date")
    resolution: str = Field(default="1D", description="Data resolution (1m, 5m, 1H, 1D)")
    
    @validator("symbol")
    def validate_symbol(cls, v):
        return v.upper()
    
    @validator("to_date")
    def validate_date_range(cls, v, values):
        if "from_date" in values and v < values["from_date"]:
            raise ValueError("to_date must be after from_date")
        return v


class TechnicalIndicatorRequest(BaseModel):
    """Request for technical indicators"""
    symbol: str = Field(..., description="Stock symbol")
    indicators: List[str] = Field(..., description="List of indicators (SMA, EMA, RSI, MACD)")
    period: int = Field(default=20, ge=1, le=200, description="Calculation period")
    
    @validator("symbol")
    def validate_symbol(cls, v):
        return v.upper()


# WebSocket Models
class WebSocketMessage(BaseModel):
    """Base WebSocket message"""
    type: str = Field(..., description="Message type")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")
    data: Dict[str, Any] = Field(..., description="Message data")


class StreamDataMessage(WebSocketMessage):
    """Real-time streaming data message"""
    symbol: str = Field(..., description="Stock symbol")
    data_type: DataTypeEnum = Field(..., description="Type of data")
    market: MarketEnum = Field(..., description="Market exchange")


# Error Models
class MarketDataError(BaseModel):
    """Market data error response"""
    error_code: str = Field(..., description="Error code")
    error_message: str = Field(..., description="Error message")
    symbol: Optional[str] = Field(None, description="Related symbol")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")


# Analytics Models
class MarketStatistics(BaseModel):
    """Market statistics and analytics"""
    market: MarketEnum = Field(..., description="Market exchange")
    stats_date: Date = Field(..., description="Statistics date")
    
    # Volume and value
    total_volume: int = Field(..., ge=0, description="Total trading volume")
    total_value: Decimal = Field(..., ge=0, description="Total trading value")
    
    # Market breadth
    advancing_stocks: int = Field(..., ge=0, description="Number of advancing stocks")
    declining_stocks: int = Field(..., ge=0, description="Number of declining stocks")
    unchanged_stocks: int = Field(..., ge=0, description="Number of unchanged stocks")
    
    # Foreign activity
    foreign_buy_volume: int = Field(default=0, ge=0, description="Foreign buy volume")
    foreign_sell_volume: int = Field(default=0, ge=0, description="Foreign sell volume")
    foreign_net_volume: int = Field(default=0, description="Foreign net volume")
    
    # Block trades
    block_trade_volume: int = Field(default=0, ge=0, description="Block trade volume")
    block_trade_value: Decimal = Field(default=0, ge=0, description="Block trade value")


class SectorPerformance(BaseModel):
    """Sector performance data"""
    sector_code: str = Field(..., description="Sector code")
    sector_name: str = Field(..., description="Sector name")
    index_value: Decimal = Field(..., ge=0, description="Sector index value")
    change_percent: Decimal = Field(..., description="Sector change percentage")
    market_cap: Decimal = Field(..., ge=0, description="Total market cap")
    volume: int = Field(..., ge=0, description="Sector trading volume")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Data timestamp")
