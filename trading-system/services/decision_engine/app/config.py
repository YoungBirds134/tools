"""
Decision Engine Configuration
Enhanced configuration for trading decision making engine
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


class DecisionStrategy(str, Enum):
    CONSERVATIVE = "CONSERVATIVE"
    MODERATE = "MODERATE"
    AGGRESSIVE = "AGGRESSIVE"
    CUSTOM = "CUSTOM"


class Settings(BaseSettings):
    """Enhanced configuration for decision engine service"""
    
    # Environment Configuration
    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        env="DECISION_ENGINE_ENVIRONMENT",
        description="Application environment"
    )
    debug: bool = Field(
        default=False,
        env="DECISION_ENGINE_DEBUG",
        description="Enable debug mode"
    )
    
    # Application Configuration
    app_name: str = Field(
        default="Decision Engine API",
        env="DECISION_ENGINE_APP_NAME",
        description="Application name"
    )
    app_version: str = Field(
        default="1.0.0",
        env="DECISION_ENGINE_APP_VERSION",
        description="Application version"
    )
    
    # Server Configuration
    host: str = Field(
        default="0.0.0.0",
        env="DECISION_ENGINE_HOST",
        description="Server host"
    )
    port: int = Field(
        default=8004,
        env="DECISION_ENGINE_PORT",
        ge=1000,
        le=65535,
        description="Server port"
    )
    workers: int = Field(
        default=1,
        env="DECISION_ENGINE_WORKERS",
        ge=1,
        description="Number of worker processes"
    )
    reload: bool = Field(
        default=False,
        env="DECISION_ENGINE_RELOAD",
        description="Enable auto-reload (development only)"
    )
    
    # External Services URLs
    market_data_service_url: str = Field(
        default="http://localhost:8001",
        env="DECISION_ENGINE_MARKET_DATA_URL",
        description="Market Data Service URL"
    )
    technical_analysis_service_url: str = Field(
        default="http://localhost:8002",
        env="DECISION_ENGINE_TECHNICAL_ANALYSIS_URL",
        description="Technical Analysis Service URL"
    )
    prediction_service_url: str = Field(
        default="http://localhost:8003",
        env="DECISION_ENGINE_PREDICTION_URL",
        description="Prediction Service URL"
    )
    risk_management_service_url: str = Field(
        default="http://localhost:8005",
        env="DECISION_ENGINE_RISK_MANAGEMENT_URL",
        description="Risk Management Service URL"
    )
    
    # Decision Making Configuration
    default_strategy: DecisionStrategy = Field(
        default=DecisionStrategy.MODERATE,
        env="DECISION_ENGINE_DEFAULT_STRATEGY",
        description="Default trading strategy"
    )
    
    decision_timeout: int = Field(
        default=30,
        env="DECISION_ENGINE_DECISION_TIMEOUT",
        ge=5,
        le=300,
        description="Decision making timeout in seconds"
    )
    
    min_confidence_threshold: float = Field(
        default=0.6,
        env="DECISION_ENGINE_MIN_CONFIDENCE",
        ge=0.1,
        le=0.99,
        description="Minimum confidence for decisions"
    )
    
    max_positions_per_symbol: int = Field(
        default=3,
        env="DECISION_ENGINE_MAX_POSITIONS_PER_SYMBOL",
        ge=1,
        le=10,
        description="Maximum positions per symbol"
    )
    
    max_daily_trades: int = Field(
        default=50,
        env="DECISION_ENGINE_MAX_DAILY_TRADES",
        ge=1,
        le=1000,
        description="Maximum trades per day"
    )
    
    # Signal Processing Configuration
    signal_aggregation_window: int = Field(
        default=300,
        env="DECISION_ENGINE_SIGNAL_WINDOW",
        ge=60,
        le=3600,
        description="Signal aggregation window in seconds"
    )
    
    signal_weight_technical: float = Field(
        default=0.4,
        env="DECISION_ENGINE_WEIGHT_TECHNICAL",
        ge=0.0,
        le=1.0,
        description="Weight for technical analysis signals"
    )
    
    signal_weight_prediction: float = Field(
        default=0.3,
        env="DECISION_ENGINE_WEIGHT_PREDICTION",
        ge=0.0,
        le=1.0,
        description="Weight for prediction signals"
    )
    
    signal_weight_market_sentiment: float = Field(
        default=0.2,
        env="DECISION_ENGINE_WEIGHT_SENTIMENT",
        ge=0.0,
        le=1.0,
        description="Weight for market sentiment"
    )
    
    signal_weight_risk: float = Field(
        default=0.1,
        env="DECISION_ENGINE_WEIGHT_RISK",
        ge=0.0,
        le=1.0,
        description="Weight for risk factors"
    )
    
    # Risk Thresholds
    max_portfolio_risk: float = Field(
        default=0.02,
        env="DECISION_ENGINE_MAX_PORTFOLIO_RISK",
        ge=0.001,
        le=0.1,
        description="Maximum portfolio risk per trade"
    )
    
    max_sector_exposure: float = Field(
        default=0.3,
        env="DECISION_ENGINE_MAX_SECTOR_EXPOSURE",
        ge=0.1,
        le=0.8,
        description="Maximum exposure per sector"
    )
    
    max_correlation_threshold: float = Field(
        default=0.7,
        env="DECISION_ENGINE_MAX_CORRELATION",
        ge=0.1,
        le=0.95,
        description="Maximum correlation between positions"
    )
    
    # Vietnamese Market Configuration
    hose_lot_size: int = Field(
        default=100,
        env="DECISION_ENGINE_HOSE_LOT_SIZE",
        description="HOSE minimum lot size"
    )
    
    hnx_lot_size: int = Field(
        default=100,
        env="DECISION_ENGINE_HNX_LOT_SIZE",
        description="HNX minimum lot size"
    )
    
    upcom_lot_size: int = Field(
        default=1000,
        env="DECISION_ENGINE_UPCOM_LOT_SIZE",
        description="UPCOM minimum lot size"
    )
    
    price_tick_size: float = Field(
        default=0.1,
        env="DECISION_ENGINE_PRICE_TICK_SIZE",
        description="Price tick size in VND"
    )
    
    # Trading Session Configuration
    trading_sessions: Dict[str, Dict[str, str]] = Field(
        default={
            "HOSE": {
                "pre_open": "08:00-08:45",
                "morning": "09:00-11:30", 
                "afternoon": "13:00-15:00",
                "close": "15:00-15:15"
            },
            "HNX": {
                "pre_open": "08:00-08:30",
                "continuous": "09:00-11:30,13:00-15:00",
                "close": "15:00-15:30"
            }
        },
        env="DECISION_ENGINE_TRADING_SESSIONS",
        description="Trading session configurations"
    )
    
    # Rule Engine Configuration
    rules_file_path: str = Field(
        default="./rules/trading_rules.json",
        env="DECISION_ENGINE_RULES_FILE",
        description="Path to trading rules configuration"
    )
    
    enable_custom_rules: bool = Field(
        default=True,
        env="DECISION_ENGINE_ENABLE_CUSTOM_RULES",
        description="Enable custom trading rules"
    )
    
    rule_execution_timeout: int = Field(
        default=10,
        env="DECISION_ENGINE_RULE_TIMEOUT",
        ge=1,
        le=60,
        description="Rule execution timeout in seconds"
    )
    
    # Decision Cache Configuration
    decision_cache_ttl: int = Field(
        default=60,
        env="DECISION_ENGINE_CACHE_TTL",
        ge=10,
        le=3600,
        description="Decision cache TTL in seconds"
    )
    
    enable_decision_caching: bool = Field(
        default=True,
        env="DECISION_ENGINE_ENABLE_CACHING",
        description="Enable decision result caching"
    )
    
    # Database Configuration
    database_url: str = Field(
        default="postgresql://decision_user:password@localhost:5432/decision_engine",
        env="DECISION_ENGINE_DATABASE_URL",
        description="Database connection URL"
    )
    database_pool_size: int = Field(
        default=10,
        env="DECISION_ENGINE_DATABASE_POOL_SIZE",
        ge=1,
        le=50,
        description="Database connection pool size"
    )
    database_echo: bool = Field(
        default=False,
        env="DECISION_ENGINE_DATABASE_ECHO",
        description="Enable database query logging"
    )
    
    # Redis Configuration
    redis_url: str = Field(
        default="redis://localhost:6379",
        env="DECISION_ENGINE_REDIS_URL",
        description="Redis connection URL"
    )
    redis_db: int = Field(
        default=4,
        env="DECISION_ENGINE_REDIS_DB",
        ge=0,
        le=15,
        description="Redis database number"
    )
    redis_password: Optional[str] = Field(
        default=None,
        env="DECISION_ENGINE_REDIS_PASSWORD",
        description="Redis password"
    )
    redis_max_connections: int = Field(
        default=20,
        env="DECISION_ENGINE_REDIS_MAX_CONNECTIONS",
        ge=1,
        description="Redis max connections"
    )
    
    # Kafka Configuration
    kafka_bootstrap_servers: List[str] = Field(
        default=["localhost:9092"],
        env="DECISION_ENGINE_KAFKA_BOOTSTRAP_SERVERS",
        description="Kafka bootstrap servers"
    )
    kafka_topic_prefix: str = Field(
        default="decision_engine",
        env="DECISION_ENGINE_KAFKA_TOPIC_PREFIX",
        description="Kafka topic prefix"
    )
    kafka_consumer_group: str = Field(
        default="decision_engine_group",
        env="DECISION_ENGINE_KAFKA_CONSUMER_GROUP",
        description="Kafka consumer group"
    )
    
    # Logging Configuration
    log_level: LogLevel = Field(
        default=LogLevel.INFO,
        env="DECISION_ENGINE_LOG_LEVEL",
        description="Logging level"
    )
    log_json: bool = Field(
        default=True,
        env="DECISION_ENGINE_LOG_JSON",
        description="Use JSON logging format"
    )
    log_file: Optional[str] = Field(
        default="logs/decision_engine.log",
        env="DECISION_ENGINE_LOG_FILE",
        description="Log file path"
    )
    
    # Rate Limiting
    rate_limit_requests: int = Field(
        default=1000,
        env="DECISION_ENGINE_RATE_LIMIT_REQUESTS",
        ge=1,
        description="Rate limit requests per window"
    )
    rate_limit_window: int = Field(
        default=60,
        env="DECISION_ENGINE_RATE_LIMIT_WINDOW",
        ge=1,
        description="Rate limit window in seconds"
    )
    
    # HTTP Client Configuration
    http_timeout: int = Field(
        default=30,
        env="DECISION_ENGINE_HTTP_TIMEOUT",
        ge=1,
        description="HTTP request timeout"
    )
    http_max_connections: int = Field(
        default=100,
        env="DECISION_ENGINE_HTTP_MAX_CONNECTIONS",
        ge=1,
        description="HTTP max connections"
    )
    http_retries: int = Field(
        default=3,
        env="DECISION_ENGINE_HTTP_RETRIES",
        ge=0,
        description="HTTP retry attempts"
    )
    
    # Circuit Breaker Configuration
    circuit_breaker_failure_threshold: int = Field(
        default=5,
        env="DECISION_ENGINE_CIRCUIT_BREAKER_FAILURE_THRESHOLD",
        ge=1,
        description="Circuit breaker failure threshold"
    )
    circuit_breaker_timeout: int = Field(
        default=60,
        env="DECISION_ENGINE_CIRCUIT_BREAKER_TIMEOUT",
        ge=1,
        description="Circuit breaker timeout in seconds"
    )
    
    # Monitoring Configuration
    enable_metrics: bool = Field(
        default=True,
        env="DECISION_ENGINE_ENABLE_METRICS",
        description="Enable metrics collection"
    )
    metrics_port: int = Field(
        default=9094,
        env="DECISION_ENGINE_METRICS_PORT",
        ge=1000,
        le=65535,
        description="Metrics server port"
    )
    
    # CORS Configuration
    allowed_origins: List[str] = Field(
        default=["*"],
        env="DECISION_ENGINE_ALLOWED_ORIGINS",
        description="CORS allowed origins"
    )
    allowed_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        env="DECISION_ENGINE_ALLOWED_METHODS",
        description="CORS allowed methods"
    )
    allowed_headers: List[str] = Field(
        default=["*"],
        env="DECISION_ENGINE_ALLOWED_HEADERS",
        description="CORS allowed headers"
    )
    
    # Feature Flags
    enable_decisions: bool = Field(
        default=True,
        env="DECISION_ENGINE_ENABLE_DECISIONS",
        description="Enable decision making"
    )
    enable_auto_trading: bool = Field(
        default=False,
        env="DECISION_ENGINE_ENABLE_AUTO_TRADING",
        description="Enable automatic trading"
    )
    enable_paper_trading: bool = Field(
        default=True,
        env="DECISION_ENGINE_ENABLE_PAPER_TRADING",
        description="Enable paper trading mode"
    )
    enable_risk_checks: bool = Field(
        default=True,
        env="DECISION_ENGINE_ENABLE_RISK_CHECKS",
        description="Enable risk management checks"
    )
    enable_audit_logging: bool = Field(
        default=True,
        env="DECISION_ENGINE_ENABLE_AUDIT_LOGGING",
        description="Enable audit logging"
    )
    enable_performance_logging: bool = Field(
        default=True,
        env="DECISION_ENGINE_ENABLE_PERFORMANCE_LOGGING",
        description="Enable performance logging"
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
    
    @validator("signal_weight_technical", "signal_weight_prediction", "signal_weight_market_sentiment", "signal_weight_risk")
    def validate_signal_weights(cls, v, values, field):
        """Validate signal weights sum to approximately 1"""
        # This is a simplified validation - in practice you'd want to ensure all weights sum to 1
        if v < 0 or v > 1:
            raise ValueError(f"Signal weight {field.name} must be between 0 and 1")
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
            "decisions": f"{self.kafka_topic_prefix}_decisions",
            "signals": f"{self.kafka_topic_prefix}_signals",
            "alerts": f"{self.kafka_topic_prefix}_alerts",
            "audit": f"{self.kafka_topic_prefix}_audit"
        }
    
    @property
    def redis_keys(self) -> Dict[str, str]:
        """Get Redis key patterns"""
        return {
            "decisions": "decision:decisions:{symbol}:{strategy}",
            "signals": "decision:signals:{symbol}",
            "rules": "decision:rules:{rule_id}",
            "cache": "decision:cache:{key}"
        }
    
    @property
    def strategy_weights(self) -> Dict[str, float]:
        """Get normalized signal weights"""
        total = (self.signal_weight_technical + self.signal_weight_prediction + 
                self.signal_weight_market_sentiment + self.signal_weight_risk)
        
        if total == 0:
            return {
                "technical": 0.25,
                "prediction": 0.25,
                "sentiment": 0.25,
                "risk": 0.25
            }
        
        return {
            "technical": self.signal_weight_technical / total,
            "prediction": self.signal_weight_prediction / total,
            "sentiment": self.signal_weight_market_sentiment / total,
            "risk": self.signal_weight_risk / total
        }


# Global settings instance
settings = Settings()
