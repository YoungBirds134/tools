"""
Configuration settings for notification service
"""

from pydantic_settings import BaseSettings
from typing import Optional, List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # App Info
    app_name: str = "Notification Service"
    app_version: str = "1.0.0"
    description: str = "Enterprise notification service for trading system"
    environment: str = "development"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8001
    workers: int = 1
    reload: bool = False
    
    # Security
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: List[str] = ["*"]
    allowed_methods: List[str] = ["*"]
    allowed_headers: List[str] = ["*"]
    
    # Database
    database_url: str = "sqlite:///./notifications.db"
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379"
    redis_db: int = 0
    redis_password: Optional[str] = None
    
    # Celery Configuration
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    
    # Telegram Bot Configuration
    telegram_bot_token: str = ""
    telegram_bot_username: str = ""
    telegram_webhook_url: str = ""
    telegram_webhook_path: str = "/api/v1/telegram/webhook"
    telegram_bot_name: str = "Trading Notification Bot"
    telegram_bot_description: str = "Professional notification bot for trading system"
    
    # Telegram Chat Configuration
    telegram_admin_chat_ids: List[str] = []
    telegram_allowed_chat_ids: List[str] = []
    telegram_default_chat_id: str = ""
    telegram_superadmin_id: str = ""
    
    # Bot Operational Settings
    enable_telegram_bot: bool = True
    enable_webhook_mode: bool = False
    enable_polling_mode: bool = True
    telegram_session_timeout_minutes: int = 30
    telegram_max_retry_attempts: int = 3
    telegram_rate_limit_messages: int = 30
    telegram_rate_limit_window_seconds: int = 60
    
    # Notification Features
    enable_trading_notifications: bool = True
    enable_market_alerts: bool = True
    enable_price_alerts: bool = True
    enable_order_notifications: bool = True
    enable_account_notifications: bool = True
    enable_system_notifications: bool = True
    
    # Message Configuration
    telegram_max_message_length: int = 4096
    telegram_default_parse_mode: str = "Markdown"
    telegram_disable_web_page_preview: bool = True
    telegram_disable_notification: bool = False
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: Optional[str] = None
    
    # External Services
    trading_service_url: str = "http://localhost:8000"
    market_data_service_url: str = "http://localhost:8002"
    
    # Monitoring
    enable_metrics: bool = True
    metrics_port: int = 9090
    health_check_interval: int = 30
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_prefix = "NS_"  # Notification Service prefix


# Global settings instance
settings = Settings()
