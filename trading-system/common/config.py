"""
Base configuration settings for Trading System microservices.
"""

from functools import lru_cache
from typing import Any, Dict, List, Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    database_url: str = Field(
        default="postgresql://trading_user:trading_pass@localhost:5432/trading_db",
        description="Database connection URL"
    )
    echo_sql: bool = Field(default=False, description="Echo SQL queries for debugging")
    pool_size: int = Field(default=10, description="Database connection pool size")
    max_overflow: int = Field(default=20, description="Maximum connection overflow")
    pool_recycle: int = Field(default=3600, description="Connection recycle time in seconds")
    
    class Config:
        env_prefix = "DB_"


class RedisSettings(BaseSettings):
    """Redis configuration settings."""
    
    host: str = Field(default="localhost", description="Redis host")
    port: int = Field(default=6379, description="Redis port")
    db: int = Field(default=0, description="Redis database number")
    password: Optional[str] = Field(default=None, description="Redis password")
    ssl: bool = Field(default=False, description="Use SSL connection")
    max_connections: int = Field(default=20, description="Maximum connections")
    decode_responses: bool = Field(default=True, description="Decode responses to string")
    
    @property
    def url(self) -> str:
        """Generate Redis URL."""
        protocol = "rediss" if self.ssl else "redis"
        auth = f":{self.password}@" if self.password else ""
        return f"{protocol}://{auth}{self.host}:{self.port}/{self.db}"
    
    class Config:
        env_prefix = "REDIS_"


class KafkaSettings(BaseSettings):
    """Kafka configuration settings."""
    
    bootstrap_servers: List[str] = Field(
        default=["localhost:9092"], 
        description="Kafka bootstrap servers"
    )
    client_id: str = Field(default="trading-system", description="Kafka client ID")
    group_id: str = Field(default="trading-group", description="Kafka consumer group ID")
    auto_offset_reset: str = Field(default="earliest", description="Auto offset reset strategy")
    enable_auto_commit: bool = Field(default=True, description="Enable auto commit")
    max_poll_records: int = Field(default=500, description="Maximum poll records")
    session_timeout_ms: int = Field(default=30000, description="Session timeout in milliseconds")
    
    @validator("bootstrap_servers", pre=True)
    def validate_bootstrap_servers(cls, v):
        if isinstance(v, str):
            return v.split(",")
        return v
    
    class Config:
        env_prefix = "KAFKA_"


class SSIFastConnectSettings(BaseSettings):
    """SSI FastConnect API configuration."""
    
    base_url: str = Field(
        default="https://fc-data.ssi.com.vn",
        description="SSI FastConnect base URL"
    )
    consumer_id: str = Field(..., description="SSI FastConnect Consumer ID")
    consumer_secret: str = Field(..., description="SSI FastConnect Consumer Secret")
    private_key: str = Field(..., description="SSI FastConnect Private Key")
    trading_base_url: str = Field(
        default="https://fc-trading.ssi.com.vn",
        description="SSI FastConnect Trading base URL"
    )
    timeout: int = Field(default=30, description="Request timeout in seconds")
    retry_count: int = Field(default=3, description="Number of retries")
    retry_delay: float = Field(default=1.0, description="Delay between retries")
    
    class Config:
        env_prefix = "SSI_"


class SecuritySettings(BaseSettings):
    """Security configuration settings."""
    
    secret_key: str = Field(..., description="JWT secret key")
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=30, 
        description="Access token expiration in minutes"
    )
    refresh_token_expire_days: int = Field(
        default=7, 
        description="Refresh token expiration in days"
    )
    bcrypt_rounds: int = Field(default=12, description="Bcrypt rounds for password hashing")
    
    class Config:
        env_prefix = "SECURITY_"


class LoggingSettings(BaseSettings):
    """Logging configuration settings."""
    
    level: str = Field(default="INFO", description="Logging level")
    format: str = Field(
        default="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        description="Log format"
    )
    file_path: Optional[str] = Field(default=None, description="Log file path")
    max_file_size: str = Field(default="10 MB", description="Maximum log file size")
    retention: str = Field(default="30 days", description="Log retention period")
    
    class Config:
        env_prefix = "LOG_"


class MonitoringSettings(BaseSettings):
    """Monitoring configuration settings."""
    
    prometheus_enabled: bool = Field(default=True, description="Enable Prometheus metrics")
    prometheus_port: int = Field(default=9090, description="Prometheus metrics port")
    health_check_timeout: int = Field(default=5, description="Health check timeout")
    
    class Config:
        env_prefix = "MONITORING_"


class BaseConfig(BaseSettings):
    """Base configuration for all microservices."""
    
    # Application
    app_name: str = Field(default="Trading System", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="development", description="Environment name")
    
    # API
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 prefix")
    docs_url: str = Field(default="/docs", description="API documentation URL")
    redoc_url: str = Field(default="/redoc", description="ReDoc documentation URL")
    openapi_url: str = Field(default="/openapi.json", description="OpenAPI schema URL")
    
    # Server
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    workers: int = Field(default=1, description="Number of worker processes")
    
    # Timeouts
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    keep_alive_timeout: int = Field(default=5, description="Keep alive timeout")
    
    # CORS
    cors_origins: List[str] = Field(
        default=["*"], 
        description="CORS allowed origins"
    )
    cors_credentials: bool = Field(default=True, description="CORS allow credentials")
    cors_methods: List[str] = Field(
        default=["*"], 
        description="CORS allowed methods"
    )
    cors_headers: List[str] = Field(
        default=["*"], 
        description="CORS allowed headers"
    )
    
    # Component settings
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    kafka: KafkaSettings = KafkaSettings()
    ssi: SSIFastConnectSettings = SSIFastConnectSettings()
    security: SecuritySettings = SecuritySettings()
    logging: LoggingSettings = LoggingSettings()
    monitoring: MonitoringSettings = MonitoringSettings()
    
    @validator("cors_origins", "cors_methods", "cors_headers", pre=True)
    def validate_cors_lists(cls, v):
        if isinstance(v, str):
            return v.split(",")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> BaseConfig:
    """Get cached application settings."""
    return BaseConfig()


def get_service_config(service_name: str, **overrides: Any) -> Dict[str, Any]:
    """Get service-specific configuration with overrides."""
    base_config = get_settings()
    service_config = base_config.dict()
    
    # Apply service-specific overrides
    service_config.update(overrides)
    service_config["app_name"] = f"{base_config.app_name} - {service_name}"
    
    return service_config
