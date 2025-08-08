"""
FC Data API schemas
"""
from typing import Optional, List, Union
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, validator, ConfigDict
from app.schemas.base import (
    BaseResponse, PaginatedRequest, DateRangeRequest, 
    Market, TradingSession, TradingStatus, SuccessResponse
)


# Authentication DTOs
class FCDataAccessTokenRequest(BaseModel):
    """FC Data access token request"""
    consumer_id: str = Field(description="Consumer ID",default="9db5f2ee570f4624a7e9e08d408c663a")
    consumer_secret: str = Field(description="Consumer Secret",default="e42fd610cdc14636bc28e17b1c8aa949")


class FCDataAccessTokenData(BaseModel):
    """FC Data access token data"""
    accessToken: str = Field(..., description="Access token for FC Data APIs")


class FCDataAccessTokenResponse(BaseModel):
    """FC Data access token response"""
    message: str = Field(..., description="Response message")
    status: Union[str, int] = Field(..., description="Response status - SSI returns 'Success'/'Error' or 200/400")
    data: FCDataAccessTokenData = Field(..., description="Token data")


# Request DTOs
class GetSecuritiesInfoRequest(PaginatedRequest):
    """Get securities info request"""
    market: Optional[Market] = Field(None, description="Market filter")
    symbol: Optional[str] = Field(None, max_length=10, description="Symbol filter")
    
    @validator('symbol')
    def validate_symbol(cls, v):
        if v:
            return v.upper().strip()
        return v


class GetSecuritiesDetailsRequest(BaseModel):
    """Get securities details request"""
    symbol: str = Field(..., max_length=10, description="Stock symbol")
    market: Optional[Market] = Field(None, description="Market")
    
    @validator('symbol')
    def validate_symbol(cls, v):
        return v.upper().strip()


class GetIndexComponentsRequest(PaginatedRequest):
    """Get index components request"""
    index_id: str = Field(..., description="Index ID")
    
    @validator('index_id')
    def validate_index_id(cls, v):
        return v.upper().strip()


class GetIndexListRequest(PaginatedRequest):
    """Get index list request"""
    market: Optional[Market] = Field(None, description="Market filter")


class GetDailyOhlcRequest(PaginatedRequest, DateRangeRequest):
    """Get daily OHLC request"""
    symbol: Optional[str] = Field(None, max_length=10, description="Stock symbol")
    market: Optional[Market] = Field(None, description="Market")
    
    @validator('symbol')
    def validate_symbol(cls, v):
        if v:
            return v.upper().strip()
        return v


class GetIntradayOhlcRequest(PaginatedRequest, DateRangeRequest):
    """Get intraday OHLC request"""
    symbol: Optional[str] = Field(None, max_length=10, description="Stock symbol")
    resolution: Optional[int] = Field(1, ge=1, description="Resolution in minutes")
    
    @validator('symbol')
    def validate_symbol(cls, v):
        if v:
            return v.upper().strip()
        return v


class GetDailyIndexRequest(PaginatedRequest, DateRangeRequest):
    """Get daily index request"""
    index_id: str = Field(..., description="Index ID")
    
    @validator('index_id')
    def validate_index_id(cls, v):
        return v.upper().strip()


class GetDailyStockPriceRequest(PaginatedRequest, DateRangeRequest):
    """Get daily stock price request"""
    symbol: Optional[str] = Field(None, max_length=10, description="Stock symbol")
    market: Optional[Market] = Field(None, description="Market")
    
    @validator('symbol')
    def validate_symbol(cls, v):
        if v:
            return v.upper().strip()
        return v


# Response DTOs
class SecurityInfo(BaseModel):
    """Security information - matches SSI API response format"""
    Symbol: str = Field(..., description="Stock symbol")
    Market: str = Field(..., description="Market")
    CompanyName: Optional[str] = Field(None, description="Company name")
    StockCode: Optional[str] = Field(None, description="Stock code")
    StockName: Optional[str] = Field(None, description="Stock name")
    StockEnName: Optional[str] = Field(None, description="Stock English name")
    StockFullName: Optional[str] = Field(None, description="Stock full name")
    
    class Config:
        populate_by_name = True  # Allow using both field names and aliases


class SecurityDetailInfo(BaseModel):
    """Individual security detail information"""
    Isin: Optional[str] = Field(None, description="ISIN code")
    Symbol: Optional[str] = Field(None, description="Stock symbol")
    SymbolName: Optional[str] = Field(None, description="Symbol name")
    SymbolEngName: Optional[str] = Field(None, description="Symbol English name")
    SecType: Optional[str] = Field(None, description="Security type")
    MarketId: Optional[str] = Field(None, description="Market ID")
    Exchange: Optional[str] = Field(None, description="Exchange")
    Issuer: Optional[str] = Field(None, description="Issuer")
    LotSize: Optional[str] = Field(None, description="Lot size")
    IssueDate: Optional[str] = Field(None, description="Issue date")
    MaturityDate: Optional[str] = Field(None, description="Maturity date")
    FirstTradingDate: Optional[str] = Field(None, description="First trading date")
    LastTradingDate: Optional[str] = Field(None, description="Last trading date")
    ContractMultiplier: Optional[str] = Field(None, description="Contract multiplier")
    SettlMethod: Optional[str] = Field(None, description="Settlement method")
    Underlying: Optional[str] = Field(None, description="Underlying")
    PutOrCall: Optional[str] = Field(None, description="Put or call")
    ExercisePrice: Optional[str] = Field(None, description="Exercise price")
    ExerciseStyle: Optional[str] = Field(None, description="Exercise style")
    ExcerciseRatio: Optional[str] = Field(None, description="Exercise ratio")
    ListedShare: Optional[str] = Field(None, description="Listed shares")
    TickPrice1: Optional[str] = Field(None, description="Tick price 1")
    TickIncrement1: Optional[str] = Field(None, description="Tick increment 1")
    TickPrice2: Optional[str] = Field(None, description="Tick price 2")
    TickIncrement2: Optional[str] = Field(None, description="Tick increment 2")
    TickPrice3: Optional[str] = Field(None, description="Tick price 3")
    TickIncrement3: Optional[str] = Field(None, description="Tick increment 3")
    TickPrice4: Optional[str] = Field(None, description="Tick price 4")
    TickIncrement4: Optional[str] = Field(None, description="Tick increment 4")
    
    class Config:
        populate_by_name = True


class SecurityDetails(BaseModel):
    """Detailed security information - matches SSI API response format"""
    RType: Optional[str] = Field(None, description="Report type")
    ReportDate: Optional[str] = Field(None, description="Report date")
    TotalNoSym: Optional[str] = Field(None, description="Total number of symbols")
    RepeatedInfo: Optional[List[SecurityDetailInfo]] = Field(None, description="Security details info")
    
    class Config:
        populate_by_name = True


class IndexComponentStock(BaseModel):
    """Individual stock component within an index"""
    Isin: Optional[str] = Field(None, description="ISIN code")
    StockSymbol: str = Field(..., description="Stock symbol", alias="symbol")
    
    class Config:
        populate_by_name = True
        allow_population_by_field_name = True


class IndexComponentData(BaseModel):
    """Index component data - matches SSI API response format"""
    IndexCode: Optional[str] = Field(None, description="Index code")
    IndexName: Optional[str] = Field(None, description="Index name")
    Exchange: Optional[str] = Field(None, description="Exchange")
    TotalSymbolNo: Optional[str] = Field(None, description="Total number of symbols")
    IndexComponent: List[IndexComponentStock] = Field(default_factory=list, description="List of stock components")
    
    class Config:
        populate_by_name = True


class IndexInfo(BaseModel):
    """Index information - matches SSI API response format"""
    IndexCode: Optional[str] = Field(None, description="Index code", alias="index_id")
    IndexName: Optional[str] = Field(None, description="Index name", alias="index_name")
    Exchange: Optional[str] = Field(None, description="Exchange")
    
    class Config:
        populate_by_name = True
        allow_population_by_field_name = True
    
    # Backward compatibility properties
    @property
    def index_id(self) -> Optional[str]:
        return self.IndexCode
        
    @property
    def index_name(self) -> Optional[str]:
        return self.IndexName


class OhlcData(BaseModel):
    """OHLC data"""
    symbol: str = Field(..., description="Stock symbol")
    market: Market = Field(..., description="Market")
    company_name: Optional[str] = Field(None, description="Company name")
    industry: Optional[str] = Field(None, description="Industry")
    trading_status: Optional[TradingStatus] = Field(None, description="Trading status")
    listing_date: Optional[str] = Field(None, description="Listing date")
    delisting_date: Optional[str] = Field(None, description="Delisting date")


class OhlcData(BaseModel):
    """OHLC data"""
    Symbol: str = Field(..., description="Stock symbol")
    Market: str = Field(..., description="Market")
    TradingDate: str = Field(..., description="Trading date (dd/mm/yyyy)")
    Time: Optional[str] = Field(None, description="Time")
    Open: Optional[str] = Field(None, description="Open price")
    High: Optional[str] = Field(None, description="High price")
    Low: Optional[str] = Field(None, description="Low price")
    Close: Optional[str] = Field(None, description="Close price")  
    Volume: Optional[str] = Field(None, description="Volume")
    Value: Optional[str] = Field(None, description="Value")
    
    model_config = ConfigDict(populate_by_name=True)
    
    # Backward compatibility properties
    @property
    def symbol(self) -> str:
        return self.Symbol
    
    @property 
    def market(self) -> str:
        return self.Market
        
    @property
    def trading_date(self) -> str:
        return self.TradingDate
        
    @property
    def open(self) -> Optional[str]:
        return self.Open
        
    @property
    def high(self) -> Optional[str]:
        return self.High
        
    @property
    def low(self) -> Optional[str]:
        return self.Low
        
    @property
    def close(self) -> Optional[str]:
        return self.Close
        
    @property
    def volume(self) -> Optional[str]:
        return self.Volume
        
    @property
    def value(self) -> Optional[str]:
        return self.Value


class IntradayOhlcData(BaseModel):
    """Intraday OHLC data (without Market field)"""
    Symbol: str = Field(..., description="Stock symbol")
    TradingDate: str = Field(..., description="Trading date (dd/mm/yyyy)")
    Time: Optional[str] = Field(None, description="Time")
    Open: Optional[str] = Field(None, description="Open price")
    High: Optional[str] = Field(None, description="High price")
    Low: Optional[str] = Field(None, description="Low price")
    Close: Optional[str] = Field(None, description="Close price")
    Volume: Optional[str] = Field(None, description="Volume")
    Value: Optional[str] = Field(None, description="Value")
    
    model_config = ConfigDict(populate_by_name=True)
    
    # Backward compatibility properties
    @property
    def symbol(self) -> str:
        return self.Symbol
        
    @property
    def trading_date(self) -> str:
        return self.TradingDate
        
    @property
    def time(self) -> Optional[str]:
        return self.Time
        
    @property
    def open(self) -> Optional[str]:
        return self.Open
        
    @property
    def high(self) -> Optional[str]:
        return self.High
        
    @property
    def low(self) -> Optional[str]:
        return self.Low
        
    @property
    def close(self) -> Optional[str]:
        return self.Close
        
    @property
    def volume(self) -> Optional[str]:
        return self.Volume
        
    @property
    def value(self) -> Optional[str]:
        return self.Value


class IndexData(BaseModel):
    """Index data"""
    index_code: str = Field(..., description="Index code", alias="IndexId")
    index_value: Optional[Decimal] = Field(None, description="Index value", alias="IndexValue")
    trading_date: str = Field(..., description="Trading date (dd/mm/yyyy)", alias="TradingDate")
    time: Optional[str] = Field(None, description="Time", alias="Time")
    change: Optional[Decimal] = Field(None, description="Change", alias="Change")
    ratio_change: Optional[Decimal] = Field(None, description="Ratio change (%)", alias="RatioChange")
    total_trade: Optional[int] = Field(None, description="Total trades", alias="TotalTrade")
    total_match_vol: Optional[int] = Field(None, description="Total match volume", alias="TotalMatchVol")
    total_match_val: Optional[Decimal] = Field(None, description="Total match value", alias="TotalMatchVal")
    type_index: Optional[str] = Field(None, description="Index type", alias="TypeIndex")
    index_name: Optional[str] = Field(None, description="Index name", alias="IndexName")
    advances: Optional[int] = Field(None, description="Advancing stocks", alias="Advances")
    no_changes: Optional[int] = Field(None, description="Unchanged stocks", alias="NoChanges")
    declines: Optional[int] = Field(None, description="Declining stocks", alias="Declines")
    ceiling: Optional[int] = Field(None, description="Ceiling stocks", alias="Ceiling")
    floor: Optional[int] = Field(None, description="Floor stocks", alias="Floor")
    total_deal_vol: Optional[int] = Field(None, description="Total deal volume", alias="TotalDealVol")
    total_deal_val: Optional[Decimal] = Field(None, description="Total deal value", alias="TotalDealVal")
    total_vol: Optional[int] = Field(None, description="Total volume", alias="TotalVol")
    total_val: Optional[Decimal] = Field(None, description="Total value", alias="TotalVal")
    trading_session: Optional[TradingSession] = Field(None, description="Trading session", alias="TradingSession")
    market: Optional[Market] = Field(None, description="Market", alias="Market")
    exchange: Optional[str] = Field(None, description="Exchange", alias="Exchange")

    model_config = ConfigDict(populate_by_name=True)


class StockPriceData(BaseModel):
    """Stock price data"""
    trading_date: str = Field(..., description="Trading date", alias="TradingDate")
    symbol: str = Field(..., description="Symbol", alias="Symbol")
    price_change: Optional[Decimal] = Field(None, description="Price change", alias="PriceChange")
    per_price_change: Optional[Decimal] = Field(None, description="Percentage price change", alias="PerPriceChange")
    ceiling_price: Optional[Decimal] = Field(None, description="Ceiling price", alias="CeilingPrice")
    floor_price: Optional[Decimal] = Field(None, description="Floor price", alias="FloorPrice")
    ref_price: Optional[Decimal] = Field(None, description="Reference price", alias="RefPrice")
    open_price: Optional[Decimal] = Field(None, description="Open price", alias="OpenPrice")
    highest_price: Optional[Decimal] = Field(None, description="Highest price", alias="HighestPrice")
    lowest_price: Optional[Decimal] = Field(None, description="Lowest price", alias="LowestPrice")
    close_price: Optional[Decimal] = Field(None, description="Close price", alias="ClosePrice")
    average_price: Optional[Decimal] = Field(None, description="Average price", alias="AveragePrice")
    close_price_adjusted: Optional[Decimal] = Field(None, description="Adjusted close price", alias="ClosePriceAdjusted")
    total_match_vol: Optional[int] = Field(None, description="Total match volume", alias="TotalMatchVol")
    total_match_val: Optional[Decimal] = Field(None, description="Total match value", alias="TotalMatchVal")
    total_deal_val: Optional[Decimal] = Field(None, description="Total deal value", alias="TotalDealVal")
    total_deal_vol: Optional[int] = Field(None, description="Total deal volume", alias="TotalDealVol")
    foreign_buy_vol_total: Optional[int] = Field(None, description="Foreign buy volume", alias="ForeignBuyVolTotal")
    foreign_current_room: Optional[int] = Field(None, description="Foreign current room", alias="ForeignCurrentRoom")
    foreign_sell_vol_total: Optional[int] = Field(None, description="Foreign sell volume", alias="ForeignSellVolTotal")
    foreign_buy_val_total: Optional[Decimal] = Field(None, description="Foreign buy value", alias="ForeignBuyValTotal")
    foreign_sell_val_total: Optional[Decimal] = Field(None, description="Foreign sell value", alias="ForeignSellValTotal")
    total_buy_trade: Optional[int] = Field(None, description="Total buy trades", alias="TotalBuyTrade")
    total_buy_trade_vol: Optional[int] = Field(None, description="Total buy trade volume", alias="TotalBuyTradeVol")
    total_sell_trade: Optional[int] = Field(None, description="Total sell trades", alias="TotalSellTrade")
    total_sell_trade_vol: Optional[int] = Field(None, description="Total sell trade volume", alias="TotalSellTradeVol")
    net_buy_sell_vol: Optional[int] = Field(None, description="Net buy/sell volume", alias="NetBuySellVol")
    net_buy_sell_val: Optional[Decimal] = Field(None, description="Net buy/sell value", alias="NetBuySellVal")
    total_traded_vol: Optional[int] = Field(None, description="Total traded volume", alias="TotalTradedVol")
    total_traded_value: Optional[Decimal] = Field(None, description="Total traded value", alias="TotalTradedValue")
    time: Optional[str] = Field(None, description="Time", alias="Time")

    model_config = ConfigDict(populate_by_name=True)


# Response models
class GetSecuritiesInfoResponse(BaseModel):
    """Get securities info response - matches SSI API format"""
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Response status - SSI returns 'Success' or 'Error'")
    data: Optional[List[SecurityInfo]] = Field(None, description="Securities data")
    totalRecord: Optional[int] = Field(None, description="Total number of records", alias="total_record")
    
    class Config:
        populate_by_name = True
    
    # Backward compatibility property
    @property
    def total_record(self) -> Optional[int]:
        return self.totalRecord


class GetSecuritiesDetailsResponse(BaseModel):
    """Get securities details response - matches SSI API format"""
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Response status - SSI returns 'Success' or 'Error'")
    data: Optional[List[SecurityDetails]] = Field(None, description="Securities details data")
    totalRecord: Optional[int] = Field(None, description="Total number of records", alias="total_record")
    
    class Config:
        populate_by_name = True
    
    # Backward compatibility property
    @property
    def total_record(self) -> Optional[int]:
        return self.totalRecord


class GetIndexComponentsResponse(BaseModel):
    """Get index components response - matches SSI API format"""
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Response status - SSI returns 'Success' or 'Error'")
    data: Optional[List[IndexComponentData]] = Field(None, description="Index components data")
    totalRecord: Optional[int] = Field(None, description="Total number of records", alias="total_record")
    
    class Config:
        populate_by_name = True
        allow_population_by_field_name = True
    
    # Backward compatibility property
    @property
    def total_record(self) -> Optional[int]:
        return self.totalRecord


class GetIndexListResponse(BaseModel):
    """Get index list response - matches SSI API format"""
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Response status - SSI returns 'Success' or 'Error'")
    data: Optional[List[IndexInfo]] = Field(None, description="Index list data")
    totalRecord: Optional[int] = Field(None, description="Total number of records", alias="total_record")
    
    class Config:
        populate_by_name = True
    
    # Backward compatibility property
    @property
    def total_record(self) -> Optional[int]:
        return self.totalRecord


class GetDailyOhlcResponse(SuccessResponse):
    """Get daily OHLC response"""
    data: Optional[List[OhlcData]] = None
    totalRecord: Optional[int] = Field(None, description="Total record count")


class GetIntradayOhlcResponse(SuccessResponse):
    """Get intraday OHLC response"""
    data: Optional[List[IntradayOhlcData]] = None
    totalRecord: Optional[int] = Field(None, description="Total record count")


class GetDailyIndexResponse(SuccessResponse):
    """Get daily index response"""
    data: Optional[List[IndexData]] = None
    totalRecord: Optional[int] = Field(None, description="Total record count")


class GetDailyStockPriceResponse(SuccessResponse):
    """Get daily stock price response"""
    data: Optional[List[StockPriceData]] = None
    totalRecord: Optional[int] = Field(None, description="Total record count")
