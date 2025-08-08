"""
FC Trading API schemas
"""
from typing import Optional, List, Dict, Any
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.schemas.base import (
    BaseResponse, Market, OrderStatus, BuySell, 
    OrderType, TwoFactorType, SuccessResponse
)


# Authentication DTOs
class AccessTokenRequest(BaseModel):
    """Access token request"""
    consumer_id: str = Field(description="Consumer ID",default="9db5f2ee570f4624a7e9e08d408c663a")
    consumer_secret: str = Field(description="Consumer Secret",default="e42fd610cdc14636bc28e17b1c8aa949")
    code: Optional[str] = Field(None, description="2FA code (required if is_save=True)")
    two_factor_type: TwoFactorType = Field(..., description="2FA type (0=PIN, 1=OTP)")
    is_save: bool = Field(..., description="Save code for session")


class GetOTPRequest(BaseModel):
    """Get OTP request"""
    consumer_id: str = Field(..., description="Consumer ID")
    consumer_secret: str = Field(..., description="Consumer Secret")


# Order DTOs
class NewOrderRequest(BaseModel):
    """New order request"""
    account: str = Field(..., description="Trading account")
    instrument_id: str = Field(..., max_length=10, description="Stock symbol")
    market: Market = Field(..., description="Market (VN for stock, VNFE for derivatives)")
    buy_sell: BuySell = Field(..., description="Buy/Sell side")
    order_type: OrderType = Field(..., description="Order type")
    price: Decimal = Field(..., ge=0, description="Order price")
    quantity: int = Field(..., gt=0, description="Order quantity")
    stop_order: bool = Field(default=False, description="Stop order flag")
    stop_price: Optional[Decimal] = Field(default=0, ge=0, description="Stop price")
    stop_type: Optional[str] = Field(default="", description="Stop type")
    stop_step: Optional[Decimal] = Field(default=0, ge=0, description="Stop step")
    loss_step: Optional[Decimal] = Field(default=0, ge=0, description="Loss step")
    profit_step: Optional[Decimal] = Field(default=0, ge=0, description="Profit step")
    device_id: Optional[str] = Field(None, description="Device ID")
    user_agent: Optional[str] = Field(None, description="User agent")
    
    @validator('instrument_id')
    def validate_instrument_id(cls, v):
        return v.upper().strip()
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class ModifyOrderRequest(BaseModel):
    """Modify order request"""
    account: str = Field(..., description="Trading account")
    order_id: str = Field(..., description="Order ID to modify")
    instrument_id: str = Field(..., max_length=10, description="Stock symbol")
    market_id: Market = Field(..., description="Market ID")
    buy_sell: BuySell = Field(..., description="Buy/Sell side")
    order_type: OrderType = Field(..., description="Order type")
    price: Decimal = Field(..., ge=0, description="New price")
    quantity: int = Field(..., gt=0, description="New quantity")
    device_id: Optional[str] = Field(None, description="Device ID")
    user_agent: Optional[str] = Field(None, description="User agent")
    
    @validator('instrument_id')
    def validate_instrument_id(cls, v):
        return v.upper().strip()
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class CancelOrderRequest(BaseModel):
    """Cancel order request"""
    account: str = Field(..., description="Trading account")
    order_id: str = Field(..., description="Order ID to cancel")
    instrument_id: str = Field(..., max_length=10, description="Stock symbol")
    market_id: Market = Field(..., description="Market ID")
    buy_sell: BuySell = Field(..., description="Buy/Sell side")
    device_id: Optional[str] = Field(None, description="Device ID")
    user_agent: Optional[str] = Field(None, description="User agent")
    
    @validator('instrument_id')
    def validate_instrument_id(cls, v):
        return v.upper().strip()
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


# Query DTOs
class OrderBookRequest(BaseModel):
    """Order book request"""
    account: str = Field(..., description="Trading account")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class OrderHistoryRequest(BaseModel):
    """Order history request"""
    account: str = Field(..., description="Trading account")
    start_date: str = Field(..., description="Start date (dd/mm/yyyy)")
    end_date: str = Field(..., description="End date (dd/mm/yyyy)")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class CashAccountBalanceRequest(BaseModel):
    """Cash account balance request"""
    account: str = Field(..., description="Trading account")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class StockPositionRequest(BaseModel):
    """Stock position request"""
    account: str = Field(..., description="Trading account")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class PortfolioRequest(BaseModel):
    """Portfolio request"""
    account: str = Field(..., description="Trading account")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class MaxBuyQtyRequest(BaseModel):
    """Max buy quantity request"""
    account: str = Field(..., description="Trading account")
    instrument_id: str = Field(..., max_length=10, description="Stock symbol")
    price: Decimal = Field(..., gt=0, description="Price")
    
    @validator('instrument_id')
    def validate_instrument_id(cls, v):
        return v.upper().strip()
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class MaxSellQtyRequest(BaseModel):
    """Max sell quantity request"""
    account: str = Field(..., description="Trading account")
    instrument_id: str = Field(..., max_length=10, description="Stock symbol")
    
    @validator('instrument_id')
    def validate_instrument_id(cls, v):
        return v.upper().strip()
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


# Response DTOs
class AccessTokenData(BaseModel):
    """Access token data"""
    access_token: Optional[str] = Field(None, description="Access token")
    accessToken: Optional[str] = Field(None, description="Access token (alternative field)")
    
    def __init__(self, **data):
        # Handle both access_token and accessToken from SSI API
        if 'accessToken' in data and 'access_token' not in data:
            data['access_token'] = data['accessToken']
        super().__init__(**data)
    
    @property
    def token(self) -> str:
        """Get the actual token value"""
        return self.access_token or self.accessToken or ""


class OrderData(BaseModel):
    """Order data"""
    unique_id: Optional[str] = Field(None, description="Unique ID")
    order_id: Optional[str] = Field(None, description="Order ID")
    buy_sell: Optional[str] = Field(None, description="Buy/Sell side")
    price: Optional[Decimal] = Field(None, description="Order price")
    quantity: Optional[int] = Field(None, description="Order quantity")
    filled_qty: Optional[int] = Field(None, description="Filled quantity")
    order_status: Optional[OrderStatus] = Field(None, description="Order status")
    market_id: Optional[str] = Field(None, description="Market ID")
    input_time: Optional[str] = Field(None, description="Input time")
    modified_time: Optional[str] = Field(None, description="Modified time")
    instrument_id: Optional[str] = Field(None, description="Instrument ID")
    order_type: Optional[str] = Field(None, description="Order type")
    cancel_qty: Optional[int] = Field(None, description="Cancelled quantity")
    avg_price: Optional[Decimal] = Field(None, description="Average price")
    is_force_sell: Optional[bool] = Field(None, description="Force sell flag")
    is_short_sell: Optional[bool] = Field(None, description="Short sell flag")
    reject_reason: Optional[str] = Field(None, description="Reject reason")


class CashAccountBalance(BaseModel):
    """Cash account balance"""
    account: Optional[str] = Field(None, description="Account")
    cash_balance: Optional[Decimal] = Field(None, description="Cash balance")
    available_cash: Optional[Decimal] = Field(None, description="Available cash")
    debt_amount: Optional[Decimal] = Field(None, description="Debt amount")
    advance_amount: Optional[Decimal] = Field(None, description="Advance amount")


class StockPosition(BaseModel):
    """Stock position"""
    account: Optional[str] = Field(None, description="Account")
    instrument_id: Optional[str] = Field(None, description="Instrument ID")
    quantity: Optional[int] = Field(None, description="Quantity")
    available_quantity: Optional[int] = Field(None, description="Available quantity")
    avg_price: Optional[Decimal] = Field(None, description="Average price")
    market_value: Optional[Decimal] = Field(None, description="Market value")


class PortfolioItem(BaseModel):
    """Portfolio item"""
    account: Optional[str] = Field(None, description="Account")
    instrument_id: Optional[str] = Field(None, description="Instrument ID")
    qty: Optional[int] = Field(None, description="Quantity")
    average_price: Optional[Decimal] = Field(None, description="Average price")
    market_price: Optional[Decimal] = Field(None, description="Current market price")
    market_value: Optional[Decimal] = Field(None, description="Market value")
    profit_loss: Optional[Decimal] = Field(None, description="Profit/Loss")
    profit_loss_percent: Optional[Decimal] = Field(None, description="Profit/Loss percentage")


# Missing Query DTOs for additional APIs
class AuditOrderBookRequest(BaseModel):
    """Audit order book request"""
    account: str = Field(..., description="Trading account")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class DerivAccountBalanceRequest(BaseModel):
    """Derivative account balance request"""
    account: str = Field(..., description="Derivative trading account")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class PPMMRAccountRequest(BaseModel):
    """PPMMR account request"""
    account: str = Field(..., description="Trading account")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class DerivPositionRequest(BaseModel):
    """Derivative position request"""
    account: str = Field(..., description="Derivative trading account")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class RateLimitRequest(BaseModel):
    """Rate limit request"""
    account: str = Field(..., description="Trading account")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


# Derivative Order DTOs
class DerivNewOrderRequest(BaseModel):
    """Derivative new order request"""
    account: str = Field(..., description="Derivative trading account")
    instrument_id: str = Field(..., max_length=10, description="Derivative symbol")
    market: Market = Field(..., description="Market (VNFE for derivatives)")
    buy_sell: BuySell = Field(..., description="Buy/Sell side")
    order_type: OrderType = Field(..., description="Order type")
    price: Decimal = Field(..., ge=0, description="Order price")
    quantity: int = Field(..., gt=0, description="Order quantity")
    device_id: Optional[str] = Field(None, description="Device ID")
    user_agent: Optional[str] = Field(None, description="User agent")
    
    @validator('instrument_id')
    def validate_instrument_id(cls, v):
        return v.upper().strip()
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class DerivCancelOrderRequest(BaseModel):
    """Derivative cancel order request"""
    account: str = Field(..., description="Derivative trading account")
    order_id: str = Field(..., description="Order ID to cancel")
    instrument_id: str = Field(..., max_length=10, description="Derivative symbol")
    market_id: Market = Field(..., description="Market ID")
    buy_sell: BuySell = Field(..., description="Buy/Sell side")
    device_id: Optional[str] = Field(None, description="Device ID")
    user_agent: Optional[str] = Field(None, description="User agent")
    
    @validator('instrument_id')
    def validate_instrument_id(cls, v):
        return v.upper().strip()
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class DerivModifyOrderRequest(BaseModel):
    """Derivative modify order request"""
    account: str = Field(..., description="Derivative trading account")
    order_id: str = Field(..., description="Order ID to modify")
    instrument_id: str = Field(..., max_length=10, description="Derivative symbol")
    market_id: Market = Field(..., description="Market ID")
    buy_sell: BuySell = Field(..., description="Buy/Sell side")
    order_type: OrderType = Field(..., description="Order type")
    price: Decimal = Field(..., ge=0, description="New price")
    quantity: int = Field(..., gt=0, description="New quantity")
    device_id: Optional[str] = Field(None, description="Device ID")
    user_agent: Optional[str] = Field(None, description="User agent")
    
    @validator('instrument_id')
    def validate_instrument_id(cls, v):
        return v.upper().strip()
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


# Cash Management DTOs
class CashInAdvanceAmountRequest(BaseModel):
    """Cash in advance amount request"""
    account: str = Field(..., description="Trading account")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class UnsettleSoldTransactionRequest(BaseModel):
    """Unsettle sold transaction request"""
    account: str = Field(..., description="Trading account")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class TransferHistoriesRequest(BaseModel):
    """Transfer histories request"""
    account: str = Field(..., description="Trading account")
    start_date: str = Field(..., description="Start date (dd/mm/yyyy)")
    end_date: str = Field(..., description="End date (dd/mm/yyyy)")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class CashInAdvanceHistoriesRequest(BaseModel):
    """Cash in advance histories request"""
    account: str = Field(..., description="Trading account")
    start_date: str = Field(..., description="Start date (dd/mm/yyyy)")
    end_date: str = Field(..., description="End date (dd/mm/yyyy)")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class EstCashInAdvanceFeeRequest(BaseModel):
    """Estimate cash in advance fee request"""
    account: str = Field(..., description="Trading account")
    amount: Decimal = Field(..., gt=0, description="Amount to advance")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class VSDCashDWRequest(BaseModel):
    """VSD cash deposit/withdraw request"""
    account: str = Field(..., description="Trading account")
    amount: Decimal = Field(..., gt=0, description="Amount")
    type: str = Field(..., description="Transaction type (D=Deposit, W=Withdraw)")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class TransferInternalRequest(BaseModel):
    """Transfer internal request"""
    from_account: str = Field(..., description="From account")
    to_account: str = Field(..., description="To account")
    amount: Decimal = Field(..., gt=0, description="Transfer amount")
    
    @validator('from_account')
    def validate_from_account(cls, v):
        return v.upper().strip()
    
    @validator('to_account')
    def validate_to_account(cls, v):
        return v.upper().strip()


class CreateCashInAdvanceRequest(BaseModel):
    """Create cash in advance request"""
    account: str = Field(..., description="Trading account")
    amount: Decimal = Field(..., gt=0, description="Advance amount")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


# Stock Transfer DTOs
class TransferableRequest(BaseModel):
    """Transferable stock request"""
    account: str = Field(..., description="Trading account")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class StockTransferHistoriesRequest(BaseModel):
    """Stock transfer histories request"""
    account: str = Field(..., description="Trading account")
    start_date: str = Field(..., description="Start date (dd/mm/yyyy)")
    end_date: str = Field(..., description="End date (dd/mm/yyyy)")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class StockTransferRequest(BaseModel):
    """Stock transfer request"""
    from_account: str = Field(..., description="From account")
    to_account: str = Field(..., description="To account")
    instrument_id: str = Field(..., max_length=10, description="Stock symbol")
    quantity: int = Field(..., gt=0, description="Transfer quantity")
    
    @validator('from_account')
    def validate_from_account(cls, v):
        return v.upper().strip()
    
    @validator('to_account')
    def validate_to_account(cls, v):
        return v.upper().strip()
    
    @validator('instrument_id')
    def validate_instrument_id(cls, v):
        return v.upper().strip()


# ORS (Order Right Subscription) DTOs
class DividendRequest(BaseModel):
    """Dividend request"""
    account: str = Field(..., description="Trading account")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class ExercisableQuantityRequest(BaseModel):
    """Exercisable quantity request"""
    account: str = Field(..., description="Trading account")
    instrument_id: str = Field(..., max_length=10, description="Stock symbol")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()
    
    @validator('instrument_id')
    def validate_instrument_id(cls, v):
        return v.upper().strip()


class ORSHistoriesRequest(BaseModel):
    """ORS histories request"""
    account: str = Field(..., description="Trading account")
    start_date: str = Field(..., description="Start date (dd/mm/yyyy)")
    end_date: str = Field(..., description="End date (dd/mm/yyyy)")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()


class ORSCreateRequest(BaseModel):
    """ORS create request"""
    account: str = Field(..., description="Trading account")
    instrument_id: str = Field(..., max_length=10, description="Stock symbol")
    quantity: int = Field(..., gt=0, description="Exercise quantity")
    
    @validator('account')
    def validate_account(cls, v):
        return v.upper().strip()
    
    @validator('instrument_id')
    def validate_instrument_id(cls, v):
        return v.upper().strip()


# Additional Response DTOs
class DerivAccountBalance(BaseModel):
    """Derivative account balance"""
    account: Optional[str] = Field(None, description="Account")
    account_balance: Optional[Decimal] = Field(None, description="Total balance")
    fee: Optional[Decimal] = Field(None, description="Fee")
    commission: Optional[Decimal] = Field(None, description="Commission")
    interest: Optional[Decimal] = Field(None, description="Interest")
    loan: Optional[Decimal] = Field(None, description="Loan")
    delivery_amount: Optional[Decimal] = Field(None, description="Delivery amount")
    margin_call: Optional[Decimal] = Field(None, description="Margin call")
    available_amount: Optional[Decimal] = Field(None, description="Available amount")
    margin_ratio: Optional[Decimal] = Field(None, description="Margin ratio")
    total_equity: Optional[Decimal] = Field(None, description="Total equity")


class PPMMRAccount(BaseModel):
    """PPMMR account data"""
    account: Optional[str] = Field(None, description="Account")
    margin_ratio: Optional[Decimal] = Field(None, description="Margin ratio")
    margin_call: Optional[Decimal] = Field(None, description="Margin call")
    maintenance_margin: Optional[Decimal] = Field(None, description="Maintenance margin")


class DerivPosition(BaseModel):
    """Derivative position"""
    account: Optional[str] = Field(None, description="Account")
    market_id: Optional[str] = Field(None, description="Market ID")
    instrument_id: Optional[str] = Field(None, description="Instrument ID")
    long_qty: Optional[int] = Field(None, description="Long quantity")
    short_qty: Optional[int] = Field(None, description="Short quantity")
    net_qty: Optional[int] = Field(None, description="Net quantity")
    avg_price: Optional[Decimal] = Field(None, description="Average price")
    market_value: Optional[Decimal] = Field(None, description="Market value")


class RateLimit(BaseModel):
    """Rate limit data"""
    endpoint: Optional[str] = Field(None, description="API endpoint")
    limit: Optional[int] = Field(None, description="Rate limit")
    period: Optional[str] = Field(None, description="Time period")


class MaxBuyQtyData(BaseModel):
    """Max buy quantity data"""
    account: Optional[str] = Field(None, description="Account")
    max_buy_qty: Optional[int] = Field(None, description="Max buy quantity")
    margin_ratio: Optional[Decimal] = Field(None, description="Margin ratio")
    purchasing_power: Optional[Decimal] = Field(None, description="Purchasing power")
    orig_margin_ratio: Optional[Decimal] = Field(None, description="Original margin ratio")


class MaxSellQtyData(BaseModel):
    """Max sell quantity data"""
    account: Optional[str] = Field(None, description="Account")
    max_sell_qty: Optional[int] = Field(None, description="Max sell quantity", alias="maxSellQty")


class CashInAdvanceAmount(BaseModel):
    """Cash in advance amount"""
    account: Optional[str] = Field(None, description="Account")
    available_amount: Optional[Decimal] = Field(None, description="Available amount")
    used_amount: Optional[Decimal] = Field(None, description="Used amount")


class TransferHistory(BaseModel):
    """Transfer history"""
    transaction_id: Optional[str] = Field(None, description="Transaction ID")
    from_account: Optional[str] = Field(None, description="From account")
    to_account: Optional[str] = Field(None, description="To account")
    amount: Optional[Decimal] = Field(None, description="Transfer amount")
    transaction_date: Optional[str] = Field(None, description="Transaction date")
    status: Optional[str] = Field(None, description="Status")


class Dividend(BaseModel):
    """Dividend data"""
    instrument_id: Optional[str] = Field(None, description="Instrument ID")
    dividend_type: Optional[str] = Field(None, description="Dividend type")
    dividend_rate: Optional[Decimal] = Field(None, description="Dividend rate")
    ex_date: Optional[str] = Field(None, description="Ex-dividend date")
    payment_date: Optional[str] = Field(None, description="Payment date")


class ExercisableQuantity(BaseModel):
    """Exercisable quantity"""
    instrument_id: Optional[str] = Field(None, description="Instrument ID")
    available_qty: Optional[int] = Field(None, description="Available quantity")
    exercised_qty: Optional[int] = Field(None, description="Exercised quantity")


class ORSHistory(BaseModel):
    """ORS history"""
    transaction_id: Optional[str] = Field(None, description="Transaction ID")
    instrument_id: Optional[str] = Field(None, description="Instrument ID")
    quantity: Optional[int] = Field(None, description="Quantity")
    exercise_date: Optional[str] = Field(None, description="Exercise date")
    status: Optional[str] = Field(None, description="Status")


# Response models
class AccessTokenResponse(SuccessResponse):
    """Access token response"""
    data: Optional[AccessTokenData] = None


class GetOTPResponse(SuccessResponse):
    """Get OTP response"""
    pass


class NewOrderResponse(SuccessResponse):
    """New order response"""
    data: Optional[OrderData] = None


class ModifyOrderResponse(SuccessResponse):
    """Modify order response"""
    data: Optional[OrderData] = None


class CancelOrderResponse(SuccessResponse):
    """Cancel order response"""
    data: Optional[OrderData] = None


class OrderBookResponse(SuccessResponse):
    """Order book response"""
    data: Optional[List[OrderData]] = None


class AuditOrderBookResponse(SuccessResponse):
    """Audit order book response"""
    data: Optional[List[OrderData]] = None


class OrderHistoryResponse(SuccessResponse):
    """Order history response"""
    data: Optional[Dict[str, Any]] = None

    @property
    def orders(self) -> Optional[List[OrderData]]:
        """Get order history list from data"""
        if self.data and "orderHistories" in self.data:
            return self.data["orderHistories"]
        return None

    @property
    def account(self) -> Optional[str]:
        """Get account from data"""
        if self.data and "account" in self.data:
            return self.data["account"]
        return None


class CashAccountBalanceResponse(SuccessResponse):
    """Cash account balance response"""
    data: Optional[CashAccountBalance] = None


class DerivAccountBalanceResponse(SuccessResponse):
    """Derivative account balance response"""
    data: Optional[DerivAccountBalance] = None


class PPMMRAccountResponse(SuccessResponse):
    """PPMMR account response"""
    data: Optional[PPMMRAccount] = None


class StockPositionResponse(SuccessResponse):
    """Stock position response"""
    data: Optional[List[StockPosition]] = None


class PortfolioResponse(SuccessResponse):
    """Portfolio response"""
    data: Optional[List[PortfolioItem]] = None


class DerivPositionResponse(SuccessResponse):
    """Derivative position response"""
    data: Optional[List[DerivPosition]] = None


class MaxBuyQtyResponse(SuccessResponse):
    """Max buy quantity response"""
    data: Optional[MaxBuyQtyData] = None


class MaxSellQtyResponse(SuccessResponse):
    """Max sell quantity response"""
    data: Optional[MaxSellQtyData] = None


class RateLimitResponse(SuccessResponse):
    """Rate limit response"""
    data: Optional[List[RateLimit]] = None


# Derivative Order Responses
class DerivNewOrderResponse(SuccessResponse):
    """Derivative new order response"""
    data: Optional[OrderData] = None


class DerivCancelOrderResponse(SuccessResponse):
    """Derivative cancel order response"""
    data: Optional[OrderData] = None


class DerivModifyOrderResponse(SuccessResponse):
    """Derivative modify order response"""
    data: Optional[OrderData] = None


# Cash Management Responses
class CashInAdvanceAmountResponse(SuccessResponse):
    """Cash in advance amount response"""
    data: Optional[CashInAdvanceAmount] = None


class UnsettleSoldTransactionResponse(SuccessResponse):
    """Unsettle sold transaction response"""
    data: Optional[List[TransferHistory]] = None


class TransferHistoriesResponse(SuccessResponse):
    """Transfer histories response"""
    data: Optional[List[TransferHistory]] = None


class CashInAdvanceHistoriesResponse(SuccessResponse):
    """Cash in advance histories response"""
    data: Optional[List[TransferHistory]] = None


class EstCashInAdvanceFeeResponse(SuccessResponse):
    """Estimate cash in advance fee response"""
    data: Optional[Decimal] = None


class VSDCashDWResponse(SuccessResponse):
    """VSD cash deposit/withdraw response"""
    data: Optional[str] = None


class TransferInternalResponse(SuccessResponse):
    """Transfer internal response"""
    data: Optional[str] = None


class CreateCashInAdvanceResponse(SuccessResponse):
    """Create cash in advance response"""
    data: Optional[str] = None


# Stock Transfer Responses
class TransferableResponse(SuccessResponse):
    """Transferable stock response"""
    data: Optional[List[StockPosition]] = None


class StockTransferHistoriesResponse(SuccessResponse):
    """Stock transfer histories response"""
    data: Optional[List[TransferHistory]] = None


class StockTransferResponse(SuccessResponse):
    """Stock transfer response"""
    data: Optional[str] = None


# ORS Responses
class DividendResponse(SuccessResponse):
    """Dividend response"""
    data: Optional[List[Dividend]] = None


class ExercisableQuantityResponse(SuccessResponse):
    """Exercisable quantity response"""
    data: Optional[ExercisableQuantity] = None


class ORSHistoriesResponse(SuccessResponse):
    """ORS histories response"""
    data: Optional[List[ORSHistory]] = None


class ORSCreateResponse(SuccessResponse):
    """ORS create response"""
    data: Optional[str] = None
