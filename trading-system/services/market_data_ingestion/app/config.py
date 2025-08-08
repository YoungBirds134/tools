"""
Market Data Ingestion Service - Configuration
Enhanced production-ready configuration for Vietnamese stock market data ingestion
"""

from typing import List, Optional, Any, Dict
from pydantic import BaseSettings, validator, Field
from enum import Enum
import os


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Enhanced configuration with Vietnamese market specifics"""
    
    # Environment Configuration
    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        env="MARKET_DATA_ENVIRONMENT",
        description="Application environment"
    )
    debug: bool = Field(
        default=False,
        env="MARKET_DATA_DEBUG",
        description="Enable debug mode"
    )
    
    # Application Configuration
    app_name: str = Field(
        default="Market Data Ingestion API",
        env="MARKET_DATA_APP_NAME",
        description="Application name"
    )
    app_version: str = Field(
        default="1.0.0",
        env="MARKET_DATA_APP_VERSION",
        description="Application version"
    )
    
    # Server Configuration
    host: str = Field(
        default="0.0.0.0",
        env="MARKET_DATA_HOST",
        description="Server host"
    )
    port: int = Field(
        default=8001,
        env="MARKET_DATA_PORT",
        ge=1000,
        le=65535,
        description="Server port"
    )
    workers: int = Field(
        default=1,
        env="MARKET_DATA_WORKERS",
        ge=1,
        description="Number of worker processes"
    )
    reload: bool = Field(
        default=False,
        env="MARKET_DATA_RELOAD",
        description="Enable auto-reload (development only)"
    )
    
    # SSI FastConnect API Configuration
    consumer_id: str = Field(
        env="MARKET_DATA_CONSUMER_ID",
        description="SSI Consumer ID"
    )
    consumer_secret: str = Field(
        env="MARKET_DATA_CONSUMER_SECRET",
        description="SSI Consumer Secret"
    )
    private_key: str = Field(
        env="MARKET_DATA_PRIVATE_KEY",
        description="Base64 encoded private key"
    )
    public_key: str = Field(
        env="MARKET_DATA_PUBLIC_KEY",
        description="Base64 encoded public key"
    )
    
    # SSI API URLs
    fc_trading_url: str = Field(
        default="https://fc-tradeapi.ssi.com.vn/",
        env="MARKET_DATA_FC_TRADING_URL",
        description="SSI Trading API URL"
    )
    fc_data_url: str = Field(
        default="https://fc-data.ssi.com.vn/",
        env="MARKET_DATA_FC_DATA_URL",
        description="SSI Data API URL"
    )
    fc_stream_url: str = Field(
        default="https://fc-datahub.ssi.com.vn/",
        env="MARKET_DATA_FC_STREAM_URL",
        description="SSI Stream API URL"
    )
    
    # Market Data Configuration
    market_symbols: List[str] = Field(
        default=["VN30", "VIC", "VCB", "FPT", "HPG", "TCB", "MSN", "BID"],
        env="MARKET_DATA_SYMBOLS",
        description="Default symbols to track"
    )
    
    data_refresh_interval: int = Field(
        default=5,
        env="MARKET_DATA_REFRESH_INTERVAL",
        ge=1,
        le=300,
        description="Data refresh interval in seconds"
    )
    
    enable_real_time: bool = Field(
        default=True,
        env="MARKET_DATA_ENABLE_REAL_TIME",
        description="Enable real-time data streaming"
    )
    
    # Database Configuration
    database_url: str = Field(
        default="postgresql://market_user:password@localhost:5432/market_data",
        env="MARKET_DATA_DATABASE_URL",
        description="Database connection URL"
    )
    database_pool_size: int = Field(
        default=10,
        env="MARKET_DATA_DATABASE_POOL_SIZE",
        ge=1,
        le=50,
        description="Database connection pool size"
    )
    database_echo: bool = Field(
        default=False,
        env="MARKET_DATA_DATABASE_ECHO",
        description="Enable database query logging"
    )
    
    # Redis Configuration
    redis_url: str = Field(
        default="redis://localhost:6379",
        env="MARKET_DATA_REDIS_URL",
        description="Redis connection URL"
    )
    redis_db: int = Field(
        default=1,
        env="MARKET_DATA_REDIS_DB",
        ge=0,
        le=15,
        description="Redis database number"
    )
    redis_password: Optional[str] = Field(
        default=None,
        env="MARKET_DATA_REDIS_PASSWORD",
        description="Redis password"
    )
    redis_max_connections: int = Field(
        default=20,
        env="MARKET_DATA_REDIS_MAX_CONNECTIONS",
        ge=1,
        description="Redis max connections"
    )
    
    # Kafka Configuration
    kafka_bootstrap_servers: List[str] = Field(
        default=["localhost:9092"],
        env="MARKET_DATA_KAFKA_BOOTSTRAP_SERVERS",
        description="Kafka bootstrap servers"
    )
    kafka_topic_prefix: str = Field(
        default="market_data",
        env="MARKET_DATA_KAFKA_TOPIC_PREFIX",
        description="Kafka topic prefix"
    )
    kafka_consumer_group: str = Field(
        default="market_data_group",
        env="MARKET_DATA_KAFKA_CONSUMER_GROUP",
        description="Kafka consumer group"
    )
    
    # Logging Configuration
    log_level: LogLevel = Field(
        default=LogLevel.INFO,
        env="MARKET_DATA_LOG_LEVEL",
        description="Logging level"
    )
    log_json: bool = Field(
        default=True,
        env="MARKET_DATA_LOG_JSON",
        description="Use JSON logging format"
    )
    log_file: Optional[str] = Field(
        default="logs/market_data.log",
        env="MARKET_DATA_LOG_FILE",
        description="Log file path"
    )
    
    # Rate Limiting
    rate_limit_requests: int = Field(
        default=200,
        env="MARKET_DATA_RATE_LIMIT_REQUESTS",
        ge=1,
        description="Rate limit requests per window"
    )
    rate_limit_window: int = Field(
        default=60,
        env="MARKET_DATA_RATE_LIMIT_WINDOW",
        ge=1,
        description="Rate limit window in seconds"
    )
    
    # HTTP Client Configuration
    http_timeout: int = Field(
        default=30,
        env="MARKET_DATA_HTTP_TIMEOUT",
        ge=1,
        description="HTTP request timeout"
    )
    http_max_connections: int = Field(
        default=100,
        env="MARKET_DATA_HTTP_MAX_CONNECTIONS",
        ge=1,
        description="HTTP max connections"
    )
    http_retries: int = Field(
        default=3,
        env="MARKET_DATA_HTTP_RETRIES",
        ge=0,
        description="HTTP retry attempts"
    )
    
    # Circuit Breaker Configuration
    circuit_breaker_failure_threshold: int = Field(
        default=5,
        env="MARKET_DATA_CIRCUIT_BREAKER_FAILURE_THRESHOLD",
        ge=1,
        description="Circuit breaker failure threshold"
    )
    circuit_breaker_timeout: int = Field(
        default=60,
        env="MARKET_DATA_CIRCUIT_BREAKER_TIMEOUT",
        ge=1,
        description="Circuit breaker timeout in seconds"
    )
    
    # Monitoring Configuration
    enable_metrics: bool = Field(
        default=True,
        env="MARKET_DATA_ENABLE_METRICS",
        description="Enable metrics collection"
    )
    metrics_port: int = Field(
        default=9091,
        env="MARKET_DATA_METRICS_PORT",
        ge=1000,
        le=65535,
        description="Metrics server port"
    )
    
    # CORS Configuration
    allowed_origins: List[str] = Field(
        default=["*"],
        env="MARKET_DATA_ALLOWED_ORIGINS",
        description="CORS allowed origins"
    )
    allowed_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        env="MARKET_DATA_ALLOWED_METHODS",
        description="CORS allowed methods"
    )
    allowed_headers: List[str] = Field(
        default=["*"],
        env="MARKET_DATA_ALLOWED_HEADERS",
        description="CORS allowed headers"
    )
    
    # Feature Flags
    enable_data_collection: bool = Field(
        default=True,
        env="MARKET_DATA_ENABLE_DATA_COLLECTION",
        description="Enable data collection"
    )
    enable_real_api: bool = Field(
        default=False,
        env="MARKET_DATA_ENABLE_REAL_API",
        description="Enable real SSI API calls"
    )
    enable_audit_logging: bool = Field(
        default=True,
        env="MARKET_DATA_ENABLE_AUDIT_LOGGING",
        description="Enable audit logging"
    )
    enable_performance_logging: bool = Field(
        default=True,
        env="MARKET_DATA_ENABLE_PERFORMANCE_LOGGING",
        description="Enable performance logging"
    )
    
    # Data Storage Configuration
    data_retention_days: int = Field(
        default=365,
        env="MARKET_DATA_RETENTION_DAYS",
        ge=1,
        description="Data retention period in days"
    )
    compression_enabled: bool = Field(
        default=True,
        env="MARKET_DATA_COMPRESSION_ENABLED",
        description="Enable data compression"
    )
    
    @validator("reload")
    def validate_reload(cls, v, values):
        """Reload only in development"""
        if v and values.get("environment") == Environment.PRODUCTION:
            raise ValueError("Reload cannot be enabled in production")
        return v
    
    @validator("debug")
    def validate_debug(cls, v, values):
        """Debug only in development/testing"""
        if v and values.get("environment") == Environment.PRODUCTION:
            raise ValueError("Debug cannot be enabled in production")
        return v
    
    @validator("allowed_origins")
    def validate_cors_origins(cls, v, values):
        """Restrict CORS origins in production"""
        if values.get("environment") == Environment.PRODUCTION and "*" in v:
            raise ValueError("Wildcard CORS origins not allowed in production")
        return v
    
    @validator("market_symbols")
    def validate_symbols(cls, v):
        """Validate symbol format"""
        for symbol in v:
            if not symbol.replace(".", "").replace("-", "").isalnum():
                raise ValueError(f"Invalid symbol format: {symbol}")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    @property
    def is_development(self) -> bool:
        return self.environment == Environment.DEVELOPMENT
    
    @property
    def is_production(self) -> bool:
        return self.environment == Environment.PRODUCTION
    
    @property
    def kafka_topics(self) -> Dict[str, str]:
        """Get Kafka topic names"""
        return {
            "market_data": f"{self.kafka_topic_prefix}_market_data",
            "price_updates": f"{self.kafka_topic_prefix}_price_updates",
            "order_book": f"{self.kafka_topic_prefix}_order_book",
            "trades": f"{self.kafka_topic_prefix}_trades"
        }


# Global settings instance
settings = Settings()
