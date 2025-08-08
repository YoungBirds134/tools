"""
Notification models for enterprise notification service
"""

from enum import Enum
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field
from datetime import datetime


class NotificationType(str, Enum):
    """Types of notifications"""
    TRADE_EXECUTED = "trade_executed"
    ORDER_FILLED = "order_filled"
    ORDER_PARTIAL_FILL = "order_partial_fill"
    ORDER_CANCELLED = "order_cancelled"
    ORDER_REJECTED = "order_rejected"
    PRICE_ALERT = "price_alert"
    VOLUME_ALERT = "volume_alert"
    MARKET_OPEN = "market_open"
    MARKET_CLOSE = "market_close"
    ACCOUNT_BALANCE_LOW = "account_balance_low"
    MARGIN_CALL = "margin_call"
    SYSTEM_MAINTENANCE = "system_maintenance"
    SECURITY_ALERT = "security_alert"
    PORTFOLIO_REPORT = "portfolio_report"


class NotificationPriority(str, Enum):
    """Notification priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class NotificationStatus(str, Enum):
    """Notification delivery status"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    EXPIRED = "expired"


class NotificationChannel(str, Enum):
    """Notification delivery channels"""
    TELEGRAM = "telegram"
    EMAIL = "email"
    SMS = "sms"
    WEBHOOK = "webhook"
    PUSH = "push"


class NotificationRequest(BaseModel):
    """Request to send a notification"""
    user_id: str
    notification_type: NotificationType
    title: str
    message: str
    priority: NotificationPriority = NotificationPriority.NORMAL
    channels: List[NotificationChannel] = [NotificationChannel.TELEGRAM]
    data: Optional[Dict[str, Any]] = None
    expires_at: Optional[datetime] = None
    schedule_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class NotificationResponse(BaseModel):
    """Response after sending notification"""
    notification_id: str
    status: NotificationStatus
    message: str
    channels_sent: List[NotificationChannel]
    sent_at: datetime
    delivery_info: Optional[Dict[str, Any]] = None


class TelegramNotification(BaseModel):
    """Telegram-specific notification"""
    chat_id: str
    message: str
    parse_mode: str = "Markdown"
    disable_web_page_preview: bool = True
    disable_notification: bool = False
    reply_markup: Optional[Dict[str, Any]] = None
    

class BulkNotificationRequest(BaseModel):
    """Request to send notifications to multiple users"""
    user_ids: List[str]
    notification_type: NotificationType
    title: str
    message: str
    priority: NotificationPriority = NotificationPriority.NORMAL
    channels: List[NotificationChannel] = [NotificationChannel.TELEGRAM]
    data: Optional[Dict[str, Any]] = None
    
    
class NotificationTemplate(BaseModel):
    """Template for notifications"""
    template_id: str
    name: str
    notification_type: NotificationType
    title_template: str
    message_template: str
    default_priority: NotificationPriority = NotificationPriority.NORMAL
    default_channels: List[NotificationChannel] = [NotificationChannel.TELEGRAM]
    variables: List[str] = []
    

class NotificationStats(BaseModel):
    """Notification statistics"""
    total_sent: int
    total_delivered: int
    total_failed: int
    delivery_rate: float
    channels_stats: Dict[str, Dict[str, int]]
    hourly_stats: Dict[str, int]
    
    
class UserNotificationSettings(BaseModel):
    """User notification preferences"""
    user_id: str
    enabled_channels: List[NotificationChannel] = [NotificationChannel.TELEGRAM]
    enabled_types: List[NotificationType] = []
    quiet_hours_start: Optional[str] = None  # Format: "HH:MM"
    quiet_hours_end: Optional[str] = None    # Format: "HH:MM"
    timezone: str = "UTC"
    minimum_priority: NotificationPriority = NotificationPriority.NORMAL
