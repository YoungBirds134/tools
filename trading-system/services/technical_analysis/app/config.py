"""
Technical Analysis Service - Configuration
Enhanced production-ready configuration for technical analysis and indicators
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
    """Enhanced configuration for technical analysis service"""
    
    # Environment Configuration
    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        env="TECHNICAL_ANALYSIS_ENVIRONMENT",
        description="Application environment"
    )
    debug: bool = Field(
        default=False,
        env="TECHNICAL_ANALYSIS_DEBUG",
        description="Enable debug mode"
    )
    
    # Application Configuration
    app_name: str = Field(
        default="Technical Analysis API",
        env="TECHNICAL_ANALYSIS_APP_NAME",
        description="Application name"
    )
    app_version: str = Field(
        default="1.0.0",
        env="TECHNICAL_ANALYSIS_APP_VERSION",
        description="Application version"
    )
    
    # Server Configuration
    host: str = Field(
        default="0.0.0.0",
        env="TECHNICAL_ANALYSIS_HOST",
        description="Server host"
    )
    port: int = Field(
        default=8002,
        env="TECHNICAL_ANALYSIS_PORT",
        ge=1000,
        le=65535,
        description="Server port"
    )
    workers: int = Field(
        default=1,
        env="TECHNICAL_ANALYSIS_WORKERS",
        ge=1,
        description="Number of worker processes"
    )
    reload: bool = Field(
        default=False,
        env="TECHNICAL_ANALYSIS_RELOAD",
        description="Enable auto-reload (development only)"
    )
    
    # External Services URLs
    market_data_service_url: str = Field(
        default="http://localhost:8001",
        env="TECHNICAL_ANALYSIS_MARKET_DATA_URL",
        description="Market Data Service URL"
    )
    
    # Technical Analysis Configuration
    default_periods: Dict[str, int] = Field(
        default={
            "sma_short": 5,
            "sma_medium": 20,
            "sma_long": 50,
            "ema_short": 12,
            "ema_long": 26,
            "rsi": 14,
            "macd_fast": 12,
            "macd_slow": 26,
            "macd_signal": 9,
            "bb_period": 20,
            "stochastic": 14,
            "adx": 14,
            "williams_r": 14,
            "cci": 20
        },
        env="TECHNICAL_ANALYSIS_DEFAULT_PERIODS",
        description="Default periods for technical indicators"
    )
    
    # Data Configuration
    max_history_days: int = Field(
        default=1000,
        env="TECHNICAL_ANALYSIS_MAX_HISTORY_DAYS",
        ge=1,
        le=5000,
        description="Maximum historical data days"
    )
    
    min_data_points: int = Field(
        default=50,
        env="TECHNICAL_ANALYSIS_MIN_DATA_POINTS",
        ge=10,
        description="Minimum data points for analysis"
    )
    
    cache_ttl_seconds: int = Field(
        default=300,
        env="TECHNICAL_ANALYSIS_CACHE_TTL",
        ge=60,
        description="Cache TTL in seconds"
    )
    
    # Pattern Recognition Configuration
    enable_pattern_recognition: bool = Field(
        default=True,
        env="TECHNICAL_ANALYSIS_ENABLE_PATTERNS",
        description="Enable candlestick pattern recognition"
    )
    
    pattern_lookback_periods: int = Field(
        default=10,
        env="TECHNICAL_ANALYSIS_PATTERN_LOOKBACK",
        ge=5,
        le=50,
        description="Lookback periods for pattern recognition"
    )
    
    # Support/Resistance Configuration
    support_resistance_periods: int = Field(
        default=20,
        env="TECHNICAL_ANALYSIS_SR_PERIODS",
        ge=10,
        le=100,
        description="Periods for support/resistance calculation"
    )
    
    support_resistance_tolerance: float = Field(
        default=0.02,
        env="TECHNICAL_ANALYSIS_SR_TOLERANCE",
        ge=0.001,
        le=0.1,
        description="Tolerance for support/resistance levels"
    )
    
    # Database Configuration
    database_url: str = Field(
        default="postgresql://technical_user:password@localhost:5432/technical_analysis",
        env="TECHNICAL_ANALYSIS_DATABASE_URL",
        description="Database connection URL"
    )
    database_pool_size: int = Field(
        default=10,
        env="TECHNICAL_ANALYSIS_DATABASE_POOL_SIZE",
        ge=1,
        le=50,
        description="Database connection pool size"
    )
    database_echo: bool = Field(
        default=False,
        env="TECHNICAL_ANALYSIS_DATABASE_ECHO",
        description="Enable database query logging"
    )
    
    # Redis Configuration
    redis_url: str = Field(
        default="redis://localhost:6379",
        env="TECHNICAL_ANALYSIS_REDIS_URL",
        description="Redis connection URL"
    )
    redis_db: int = Field(
        default=2,
        env="TECHNICAL_ANALYSIS_REDIS_DB",
        ge=0,
        le=15,
        description="Redis database number"
    )
    redis_password: Optional[str] = Field(
        default=None,
        env="TECHNICAL_ANALYSIS_REDIS_PASSWORD",
        description="Redis password"
    )
    redis_max_connections: int = Field(
        default=20,
        env="TECHNICAL_ANALYSIS_REDIS_MAX_CONNECTIONS",
        ge=1,
        description="Redis max connections"
    )
    
    # Kafka Configuration
    kafka_bootstrap_servers: List[str] = Field(
        default=["localhost:9092"],
        env="TECHNICAL_ANALYSIS_KAFKA_BOOTSTRAP_SERVERS",
        description="Kafka bootstrap servers"
    )
    kafka_topic_prefix: str = Field(
        default="technical_analysis",
        env="TECHNICAL_ANALYSIS_KAFKA_TOPIC_PREFIX",
        description="Kafka topic prefix"
    )
    kafka_consumer_group: str = Field(
        default="technical_analysis_group",
        env="TECHNICAL_ANALYSIS_KAFKA_CONSUMER_GROUP",
        description="Kafka consumer group"
    )
    
    # Logging Configuration
    log_level: LogLevel = Field(
        default=LogLevel.INFO,
        env="TECHNICAL_ANALYSIS_LOG_LEVEL",
        description="Logging level"
    )
    log_json: bool = Field(
        default=True,
        env="TECHNICAL_ANALYSIS_LOG_JSON",
        description="Use JSON logging format"
    )
    log_file: Optional[str] = Field(
        default="logs/technical_analysis.log",
        env="TECHNICAL_ANALYSIS_LOG_FILE",
        description="Log file path"
    )
    
    # Rate Limiting
    rate_limit_requests: int = Field(
        default=1000,
        env="TECHNICAL_ANALYSIS_RATE_LIMIT_REQUESTS",
        ge=1,
        description="Rate limit requests per window"
    )
    rate_limit_window: int = Field(
        default=60,
        env="TECHNICAL_ANALYSIS_RATE_LIMIT_WINDOW",
        ge=1,
        description="Rate limit window in seconds"
    )
    
    # HTTP Client Configuration
    http_timeout: int = Field(
        default=30,
        env="TECHNICAL_ANALYSIS_HTTP_TIMEOUT",
        ge=1,
        description="HTTP request timeout"
    )
    http_max_connections: int = Field(
        default=100,
        env="TECHNICAL_ANALYSIS_HTTP_MAX_CONNECTIONS",
        ge=1,
        description="HTTP max connections"
    )
    http_retries: int = Field(
        default=3,
        env="TECHNICAL_ANALYSIS_HTTP_RETRIES",
        ge=0,
        description="HTTP retry attempts"
    )
    
    # Circuit Breaker Configuration
    circuit_breaker_failure_threshold: int = Field(
        default=5,
        env="TECHNICAL_ANALYSIS_CIRCUIT_BREAKER_FAILURE_THRESHOLD",
        ge=1,
        description="Circuit breaker failure threshold"
    )
    circuit_breaker_timeout: int = Field(
        default=60,
        env="TECHNICAL_ANALYSIS_CIRCUIT_BREAKER_TIMEOUT",
        ge=1,
        description="Circuit breaker timeout in seconds"
    )
    
    # Monitoring Configuration
    enable_metrics: bool = Field(
        default=True,
        env="TECHNICAL_ANALYSIS_ENABLE_METRICS",
        description="Enable metrics collection"
    )
    metrics_port: int = Field(
        default=9092,
        env="TECHNICAL_ANALYSIS_METRICS_PORT",
        ge=1000,
        le=65535,
        description="Metrics server port"
    )
    
    # CORS Configuration
    allowed_origins: List[str] = Field(
        default=["*"],
        env="TECHNICAL_ANALYSIS_ALLOWED_ORIGINS",
        description="CORS allowed origins"
    )
    allowed_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        env="TECHNICAL_ANALYSIS_ALLOWED_METHODS",
        description="CORS allowed methods"
    )
    allowed_headers: List[str] = Field(
        default=["*"],
        env="TECHNICAL_ANALYSIS_ALLOWED_HEADERS",
        description="CORS allowed headers"
    )
    
    # Feature Flags
    enable_analysis: bool = Field(
        default=True,
        env="TECHNICAL_ANALYSIS_ENABLE_ANALYSIS",
        description="Enable technical analysis calculations"
    )
    enable_backtesting: bool = Field(
        default=True,
        env="TECHNICAL_ANALYSIS_ENABLE_BACKTESTING",
        description="Enable backtesting functionality"
    )
    enable_alerts: bool = Field(
        default=True,
        env="TECHNICAL_ANALYSIS_ENABLE_ALERTS",
        description="Enable technical alerts"
    )
    enable_audit_logging: bool = Field(
        default=True,
        env="TECHNICAL_ANALYSIS_ENABLE_AUDIT_LOGGING",
        description="Enable audit logging"
    )
    enable_performance_logging: bool = Field(
        default=True,
        env="TECHNICAL_ANALYSIS_ENABLE_PERFORMANCE_LOGGING",
        description="Enable performance logging"
    )
    
    # Chart Configuration
    chart_width: int = Field(
        default=800,
        env="TECHNICAL_ANALYSIS_CHART_WIDTH",
        ge=400,
        le=2000,
        description="Default chart width"
    )
    chart_height: int = Field(
        default=600,
        env="TECHNICAL_ANALYSIS_CHART_HEIGHT",
        ge=300,
        le=1500,
        description="Default chart height"
    )
    
    # Optimization Configuration
    max_concurrent_calculations: int = Field(
        default=10,
        env="TECHNICAL_ANALYSIS_MAX_CONCURRENT",
        ge=1,
        le=50,
        description="Maximum concurrent calculations"
    )
    
    calculation_timeout: int = Field(
        default=300,
        env="TECHNICAL_ANALYSIS_CALCULATION_TIMEOUT",
        ge=30,
        description="Calculation timeout in seconds"
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
    
    @validator("default_periods")
    def validate_periods(cls, v):
        """Validate technical indicator periods"""
        for indicator, period in v.items():
            if period < 1 or period > 200:
                raise ValueError(f"Invalid period for {indicator}: {period}")
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
            "analysis_results": f"{self.kafka_topic_prefix}_analysis_results",
            "alerts": f"{self.kafka_topic_prefix}_alerts",
            "signals": f"{self.kafka_topic_prefix}_signals",
            "patterns": f"{self.kafka_topic_prefix}_patterns"
        }
    
    @property
    def redis_keys(self) -> Dict[str, str]:
        """Get Redis key patterns"""
        return {
            "indicators": "ta:indicators:{symbol}:{timeframe}",
            "patterns": "ta:patterns:{symbol}:{timeframe}",
            "signals": "ta:signals:{symbol}",
            "cache": "ta:cache:{key}"
        }


# Global settings instance
settings = Settings()
