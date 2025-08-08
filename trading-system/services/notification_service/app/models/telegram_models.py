from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from datetime import datetime


class TelegramUserState(str, Enum):
    """User states for conversation flow"""
    START = "start"
    MAIN_MENU = "main_menu"
    AUTH_MENU = "auth_menu"
    WAITING_OTP = "waiting_otp"
    WAITING_CODE = "waiting_code"
    ORDER_MENU = "order_menu"
    PLACE_ORDER = "place_order"
    MODIFY_ORDER = "modify_order"
    CANCEL_ORDER = "cancel_order"
    ACCOUNT_MENU = "account_menu"
    HELP_MENU = "help_menu"
    
    # New trading flow states
    CREATING_BUY_ORDER = "creating_buy_order"
    CREATING_SELL_ORDER = "creating_sell_order"
    CREATING_PRICE_ALERT = "creating_price_alert"
    CREATING_VOLUME_ALERT = "creating_volume_alert"
    PORTFOLIO_MENU = "portfolio_menu"
    MARKET_DATA_MENU = "market_data_menu"
    ALERTS_MENU = "alerts_menu"
    CONFIRMING_ORDER = "confirming_order"
    MODIFYING_ORDER = "modifying_order"
    SETTING_STOP_LOSS = "setting_stop_loss"
    SETTING_TAKE_PROFIT = "setting_take_profit"


class OrderAction(str, Enum):
    """Order actions"""
    NEW_STOCK = "new_stock"
    NEW_DERIVATIVE = "new_derivative"
    MODIFY_STOCK = "modify_stock"
    MODIFY_DERIVATIVE = "modify_derivative"
    CANCEL_STOCK = "cancel_stock"
    CANCEL_DERIVATIVE = "cancel_derivative"


class AccountAction(str, Enum):
    """Account actions"""
    STOCK_BALANCE = "stock_balance"
    DERIVATIVE_BALANCE = "derivative_balance"
    STOCK_POSITION = "stock_position"
    DERIVATIVE_POSITION = "derivative_position"
    ORDER_HISTORY = "order_history"
    ORDER_BOOK = "order_book"


class AlertType(str, Enum):
    """Alert types"""
    PRICE_ABOVE = "price_above"
    PRICE_BELOW = "price_below"
    VOLUME_HIGH = "volume_high"
    VOLUME_LOW = "volume_low"
    PERCENTAGE_CHANGE = "percentage_change"
    MARKET_OPEN = "market_open"
    MARKET_CLOSE = "market_close"
    ORDER_FILLED = "order_filled"
    ORDER_CANCELLED = "order_cancelled"


class OrderStatus(str, Enum):
    """Order status"""
    PENDING = "pending"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    EXPIRED = "expired"


class MarketStatus(str, Enum):
    """Market status"""
    OPEN = "open"
    CLOSED = "closed"
    PRE_OPEN = "pre_open"
    POST_CLOSE = "post_close"
    SUSPENDED = "suspended"


# Telegram Models
class TelegramUser(BaseModel):
    """Telegram user model"""
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = "en"
    is_authenticated: bool = False
    fc_account: Optional[str] = None
    state: TelegramUserState = TelegramUserState.START
    temp_data: Dict[str, Any] = {}
    order_form: Optional['OrderFormData'] = None
    current_alert_data: Optional[Dict[str, Any]] = None
    preferences: Dict[str, Any] = {}
    session_start_time: Optional[datetime] = None
    last_activity: Optional[datetime] = None


class TelegramMessage(BaseModel):
    """Telegram message model"""
    message_id: int
    chat_id: int
    user_id: int
    text: Optional[str] = None
    callback_data: Optional[str] = None


class OrderFormData(BaseModel):
    """Order form data model"""
    instrument_id: Optional[str] = None
    market: Optional[str] = None
    buy_sell: Optional[str] = None
    order_type: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    account: Optional[str] = None
    order_id: Optional[str] = None  # For modify/cancel
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    
    def is_complete(self) -> bool:
        """Check if all required fields are filled"""
        required_fields = ['instrument_id', 'market', 'buy_sell', 'order_type', 'price', 'quantity']
        return all(getattr(self, field) is not None for field in required_fields)


class TradingAlert(BaseModel):
    """Trading alert model"""
    alert_id: Optional[str] = None
    user_id: int
    symbol: str
    alert_type: AlertType
    target_price: Optional[float] = None
    target_volume: Optional[int] = None
    percentage_threshold: Optional[float] = None
    is_active: bool = True
    created_at: datetime
    triggered_at: Optional[datetime] = None
    message: Optional[str] = None


class MarketData(BaseModel):
    """Market data model"""
    symbol: str
    current_price: float
    previous_close: float
    change: float
    change_percent: float
    volume: int
    high: float
    low: float
    open_price: float
    market_cap: Optional[float] = None
    timestamp: datetime


class PortfolioItem(BaseModel):
    """Portfolio item model"""
    symbol: str
    quantity: int
    average_price: float
    current_price: float
    market_value: float
    unrealized_pnl: float
    unrealized_pnl_percent: float
    last_updated: datetime


class TradingSession(BaseModel):
    """Trading session model"""
    user_id: int
    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    orders_placed: int = 0
    total_volume: float = 0
    is_active: bool = True


class TelegramCallback(BaseModel):
    """Telegram callback data model"""
    action: str
    data: Optional[str] = None
    page: int = 0


class NotificationSettings(BaseModel):
    """User notification settings"""
    user_id: int
    order_confirmations: bool = True
    price_alerts: bool = True
    market_updates: bool = True
    error_notifications: bool = True
    daily_summary: bool = False
    weekly_report: bool = False


class TradingLimits(BaseModel):
    """Trading limits model"""
    user_id: int
    max_order_value: float
    max_daily_orders: int
    max_position_size: float
    require_confirmation: bool = True
    allow_margin_trading: bool = False
    allow_derivatives: bool = False


class UserPreferences(BaseModel):
    """User preferences model"""
    user_id: int
    language: str = "en"
    timezone: str = "Asia/Ho_Chi_Minh"
    currency_display: str = "VND"
    chart_timeframe: str = "1D"
    notification_time: str = "09:00"
    auto_logout_minutes: int = 30


class TelegramCommand(BaseModel):
    """Telegram command model"""
    command: str
    description: str
    handler: str
    is_admin_only: bool = False
    is_enabled: bool = True


class TelegramBotStats(BaseModel):
    """Telegram bot statistics"""
    total_users: int
    active_users: int
    orders_today: int
    messages_today: int
    errors_today: int
    uptime_seconds: int
    last_restart: datetime
