"""
Enhanced configuration management with validation and security
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Optional, List
import os
import base64
import binascii
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def validate_private_key(private_key: str) -> bool:
    """Validate if private key is valid Base64"""
    if not private_key or private_key.strip() in ["", "your_private_key_here"]:
        return False
    
    try:
        # Try to decode the private key to check if it's valid Base64
        base64.b64decode(private_key.encode('utf-8'))
        return True
    except (binascii.Error, ValueError):
        return False


def get_safe_private_key(private_key: str) -> Optional[str]:
    """Get safe private key or None if invalid"""
    if validate_private_key(private_key):
        return private_key
    
    logger.warning("Invalid or placeholder private key detected. FC Trading client will not be initialized.")
    return None


class Settings(BaseSettings):
    """Enhanced settings with comprehensive validation and documentation"""
    
    # Environment Configuration
    environment: str = Field(default="development", description="Application environment")
    debug: bool = Field(default=False, description="Enable debug mode")
    
    # API Configuration
    app_name: str = Field(default="FC Trading API", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    app_description: str = Field(
        default="Professional FastAPI application for SSI FastConnect Trading",
        description="Application description"
    )
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, ge=1, le=65535, description="Server port")
    workers: int = Field(default=1, ge=1, le=10, description="Number of worker processes")
    reload: bool = Field(default=False, description="Enable auto-reload for development")
    
    # SSI FastConnect Configuration
    consumer_id: str = Field(default="", description="SSI Consumer ID")
    consumer_secret: str = Field(default="", description="SSI Consumer Secret")
    private_key: str = Field(default="", description="SSI Private Key (Base64)")
    public_key: str = Field(default="", description="SSI Public Key (Base64)")
    
    # SSI API URLs
    fc_trading_url: str = Field(
        default="https://fc-tradeapi.ssi.com.vn/",
        description="SSI FastConnect Trading API URL"
    )
    fc_data_url: str = Field(
        default="https://fc-data.ssi.com.vn/",
        description="SSI FastConnect Data API URL"
    )
    fc_trading_stream_url: str = Field(
        default="https://fc-tradehub.ssi.com.vn/",
        description="SSI FastConnect Trading Stream URL"
    )
    
    # Authentication Configuration
    two_fa_type: int = Field(default=1, ge=0, le=1, description="2FA Type: 0=PIN, 1=OTP")
    notify_id: str = Field(default="-1", description="Notification ID for stream connection")
    
    # Account Configuration (for development/testing)
    default_account_id: str = Field(default="", description="Default trading account ID")
    account_type: str = Field(default="VNDS", description="Account type")
    account_currency: str = Field(default="VND", description="Account currency")
    
    # Security Configuration
    secret_key: str = Field(
        default="your-secret-key-here-change-in-production",
        min_length=32,
        description="JWT secret key"
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=30, 
        ge=5, 
        le=1440, 
        description="Access token expiry in minutes"
    )
    
    # CORS Configuration
    allowed_origins: List[str] = Field(
        default=["*"], 
        description="Allowed CORS origins"
    )
    allowed_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="Allowed HTTP methods"
    )
    allowed_headers: List[str] = Field(
        default=["*"],
        description="Allowed headers"
    )
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    log_json: bool = Field(default=True, description="Use JSON logging format")
    log_file: str = Field(default="logs/app.log", description="Log file path")
    
    # Rate Limiting Configuration  
    rate_limit_requests: int = Field(
        default=100, 
        ge=1, 
        le=1000, 
        description="Max requests per window"
    )
    rate_limit_window: int = Field(
        default=60, 
        ge=1, 
        le=3600, 
        description="Rate limit window in seconds"
    )
    
    # Database Configuration
    database_url: str = Field(
        default="postgresql://user:password@localhost:5432/trading_db",
        description="Database connection URL"
    )
    database_pool_size: int = Field(default=5, ge=1, le=20, description="Database pool size")
    database_echo: bool = Field(default=False, description="Echo SQL queries")
    
    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379", description="Redis connection URL")
    redis_db: int = Field(default=0, ge=0, le=15, description="Redis database number")
    redis_password: str = Field(default="", description="Redis password")
    redis_max_connections: int = Field(default=10, ge=1, le=100, description="Redis max connections")
    
    # Kafka Configuration (for event streaming)
    kafka_bootstrap_servers: List[str] = Field(
        default=["localhost:9092"],
        description="Kafka bootstrap servers"
    )
    kafka_topic_prefix: str = Field(default="trading", description="Kafka topic prefix")
    
    # HTTP Client Configuration
    http_timeout: int = Field(default=30, ge=1, le=300, description="HTTP timeout in seconds")
    http_max_connections: int = Field(default=20, ge=1, le=100, description="Max HTTP connections")
    http_retries: int = Field(default=3, ge=0, le=10, description="Number of HTTP retries")
    
    # Circuit Breaker Configuration
    circuit_breaker_failure_threshold: int = Field(
        default=5, 
        ge=1, 
        le=20, 
        description="Circuit breaker failure threshold"
    )
    circuit_breaker_timeout: int = Field(
        default=60, 
        ge=1, 
        le=300, 
        description="Circuit breaker timeout in seconds"
    )
    
    # Monitoring Configuration
    enable_metrics: bool = Field(default=True, description="Enable Prometheus metrics")
    metrics_port: int = Field(default=9090, ge=1024, le=65535, description="Metrics server port")
    
    # Feature Flags
    enable_trading: bool = Field(default=True, description="Enable trading functionality")
    enable_real_api: bool = Field(default=False, description="Enable real SSI API calls")
    enable_audit_logging: bool = Field(default=True, description="Enable audit logging")
    enable_performance_logging: bool = Field(default=True, description="Enable performance logging")
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        """Validate secret key security"""
        if v == "your-secret-key-here-change-in-production":
            if os.getenv("ENVIRONMENT", "development") == "production":
                raise ValueError("Secret key must be changed in production")
        return v
    
    @validator('log_level')
    def validate_log_level(cls, v):
        """Validate log level"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()
    
    @validator('allowed_origins')
    def validate_cors_origins(cls, v):
        """Validate CORS origins for production"""
        if "*" in v and os.getenv("ENVIRONMENT") == "production":
            logger.warning("Wildcard CORS origins detected in production - security risk!")
        return v
    
    @property
    def is_private_key_valid(self) -> bool:
        """Check if private key is valid"""
        return validate_private_key(self.private_key)
    
    @property
    def safe_private_key(self) -> Optional[str]:
        """Get safe private key or None if invalid"""
        return get_safe_private_key(self.private_key)
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment.lower() == "development"
    
    @property
    def log_dir(self) -> Path:
        """Get log directory path"""
        return Path(self.log_file).parent
    
    def get_database_config(self) -> dict:
        """Get database configuration"""
        return {
            "url": self.database_url,
            "pool_size": self.database_pool_size,
            "echo": self.database_echo and self.debug
        }
    
    def get_redis_config(self) -> dict:
        """Get Redis configuration"""
        return {
            "url": self.redis_url,
            "db": self.redis_db,
            "password": self.redis_password if self.redis_password else None,
            "max_connections": self.redis_max_connections
        }
    
    def get_ssi_config(self) -> dict:
        """Get SSI API configuration"""
        return {
            "consumer_id": self.consumer_id,
            "consumer_secret": self.consumer_secret,
            "private_key": self.safe_private_key,
            "public_key": self.public_key,
            "trading_url": self.fc_trading_url,
            "data_url": self.fc_data_url,
            "stream_url": self.fc_trading_stream_url,
            "two_fa_type": self.two_fa_type,
            "notify_id": self.notify_id
        }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Environment variable prefix
        env_prefix = "TRADING_"


# Create global settings instance
settings = Settings()

# Validate critical settings on startup
if settings.is_production:
    required_fields = [
        "consumer_id", 
        "consumer_secret", 
        "private_key"
    ]
    
    missing_fields = [
        field for field in required_fields 
        if not getattr(settings, field)
    ]
    
    if missing_fields:
        logger.error(f"Missing required production settings: {missing_fields}")
        raise ValueError(f"Missing required production settings: {missing_fields}")

logger.info(f"Configuration loaded for environment: {settings.environment}")
