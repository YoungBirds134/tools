"""
Prediction Service Configuration
Enhanced configuration for AI/ML price prediction service
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


class ModelType(str, Enum):
    LSTM = "LSTM"
    TRANSFORMER = "TRANSFORMER"
    XGBOOST = "XGBOOST"
    LIGHTGBM = "LIGHTGBM"
    PROPHET = "PROPHET"
    ARIMA = "ARIMA"
    ENSEMBLE = "ENSEMBLE"


class Settings(BaseSettings):
    """Enhanced configuration for prediction service"""
    
    # Environment Configuration
    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        env="PREDICTION_ENVIRONMENT",
        description="Application environment"
    )
    debug: bool = Field(
        default=False,
        env="PREDICTION_DEBUG",
        description="Enable debug mode"
    )
    
    # Application Configuration
    app_name: str = Field(
        default="Prediction Service API",
        env="PREDICTION_APP_NAME",
        description="Application name"
    )
    app_version: str = Field(
        default="1.0.0",
        env="PREDICTION_APP_VERSION",
        description="Application version"
    )
    
    # Server Configuration
    host: str = Field(
        default="0.0.0.0",
        env="PREDICTION_HOST",
        description="Server host"
    )
    port: int = Field(
        default=8003,
        env="PREDICTION_PORT",
        ge=1000,
        le=65535,
        description="Server port"
    )
    workers: int = Field(
        default=1,
        env="PREDICTION_WORKERS",
        ge=1,
        description="Number of worker processes"
    )
    reload: bool = Field(
        default=False,
        env="PREDICTION_RELOAD",
        description="Enable auto-reload (development only)"
    )
    
    # External Services URLs
    market_data_service_url: str = Field(
        default="http://localhost:8001",
        env="PREDICTION_MARKET_DATA_URL",
        description="Market Data Service URL"
    )
    technical_analysis_service_url: str = Field(
        default="http://localhost:8002",
        env="PREDICTION_TECHNICAL_ANALYSIS_URL",
        description="Technical Analysis Service URL"
    )
    
    # Model Configuration
    default_model_type: ModelType = Field(
        default=ModelType.ENSEMBLE,
        env="PREDICTION_DEFAULT_MODEL_TYPE",
        description="Default prediction model type"
    )
    
    model_storage_path: str = Field(
        default="./models",
        env="PREDICTION_MODEL_STORAGE_PATH",
        description="Path to store trained models"
    )
    
    # Feature Engineering Configuration
    lookback_periods: int = Field(
        default=60,
        env="PREDICTION_LOOKBACK_PERIODS",
        ge=10,
        le=500,
        description="Historical periods to use for features"
    )
    
    feature_columns: List[str] = Field(
        default=[
            "open", "high", "low", "close", "volume",
            "sma_5", "sma_20", "sma_50", "ema_12", "ema_26",
            "rsi", "macd", "bb_upper", "bb_lower", "stochastic_k"
        ],
        env="PREDICTION_FEATURE_COLUMNS",
        description="Features to use for prediction"
    )
    
    target_horizons: List[int] = Field(
        default=[1, 3, 7, 14, 30],
        env="PREDICTION_TARGET_HORIZONS",
        description="Prediction horizons in days"
    )
    
    # Training Configuration
    train_test_split_ratio: float = Field(
        default=0.8,
        env="PREDICTION_TRAIN_TEST_SPLIT",
        ge=0.1,
        le=0.9,
        description="Train/test split ratio"
    )
    
    validation_split_ratio: float = Field(
        default=0.2,
        env="PREDICTION_VALIDATION_SPLIT",
        ge=0.1,
        le=0.5,
        description="Validation split ratio"
    )
    
    batch_size: int = Field(
        default=32,
        env="PREDICTION_BATCH_SIZE",
        ge=8,
        le=512,
        description="Training batch size"
    )
    
    epochs: int = Field(
        default=100,
        env="PREDICTION_EPOCHS",
        ge=10,
        le=1000,
        description="Training epochs"
    )
    
    learning_rate: float = Field(
        default=0.001,
        env="PREDICTION_LEARNING_RATE",
        ge=0.0001,
        le=0.1,
        description="Learning rate"
    )
    
    # Model Parameters
    lstm_units: int = Field(
        default=50,
        env="PREDICTION_LSTM_UNITS",
        ge=10,
        le=500,
        description="LSTM units"
    )
    
    lstm_layers: int = Field(
        default=2,
        env="PREDICTION_LSTM_LAYERS",
        ge=1,
        le=10,
        description="Number of LSTM layers"
    )
    
    dropout_rate: float = Field(
        default=0.2,
        env="PREDICTION_DROPOUT_RATE",
        ge=0.0,
        le=0.8,
        description="Dropout rate"
    )
    
    xgboost_n_estimators: int = Field(
        default=100,
        env="PREDICTION_XGBOOST_N_ESTIMATORS",
        ge=10,
        le=1000,
        description="XGBoost number of estimators"
    )
    
    xgboost_max_depth: int = Field(
        default=6,
        env="PREDICTION_XGBOOST_MAX_DEPTH",
        ge=3,
        le=20,
        description="XGBoost max depth"
    )
    
    # Ensemble Configuration
    ensemble_models: List[str] = Field(
        default=["LSTM", "XGBOOST", "LIGHTGBM"],
        env="PREDICTION_ENSEMBLE_MODELS",
        description="Models to include in ensemble"
    )
    
    ensemble_weights: Dict[str, float] = Field(
        default={"LSTM": 0.4, "XGBOOST": 0.3, "LIGHTGBM": 0.3},
        env="PREDICTION_ENSEMBLE_WEIGHTS",
        description="Ensemble model weights"
    )
    
    # Prediction Configuration
    prediction_interval: int = Field(
        default=300,
        env="PREDICTION_INTERVAL",
        ge=60,
        description="Prediction update interval in seconds"
    )
    
    confidence_threshold: float = Field(
        default=0.7,
        env="PREDICTION_CONFIDENCE_THRESHOLD",
        ge=0.5,
        le=0.99,
        description="Minimum confidence threshold for predictions"
    )
    
    max_prediction_age: int = Field(
        default=3600,
        env="PREDICTION_MAX_AGE",
        ge=300,
        description="Maximum age of predictions in seconds"
    )
    
    # Data Configuration
    min_training_samples: int = Field(
        default=1000,
        env="PREDICTION_MIN_TRAINING_SAMPLES",
        ge=100,
        description="Minimum training samples required"
    )
    
    max_training_samples: int = Field(
        default=10000,
        env="PREDICTION_MAX_TRAINING_SAMPLES",
        ge=1000,
        description="Maximum training samples to use"
    )
    
    data_preprocessing_steps: List[str] = Field(
        default=["normalize", "remove_outliers", "fill_missing"],
        env="PREDICTION_PREPROCESSING_STEPS",
        description="Data preprocessing steps"
    )
    
    # Database Configuration
    database_url: str = Field(
        default="postgresql://prediction_user:password@localhost:5432/prediction_service",
        env="PREDICTION_DATABASE_URL",
        description="Database connection URL"
    )
    database_pool_size: int = Field(
        default=10,
        env="PREDICTION_DATABASE_POOL_SIZE",
        ge=1,
        le=50,
        description="Database connection pool size"
    )
    database_echo: bool = Field(
        default=False,
        env="PREDICTION_DATABASE_ECHO",
        description="Enable database query logging"
    )
    
    # Redis Configuration
    redis_url: str = Field(
        default="redis://localhost:6379",
        env="PREDICTION_REDIS_URL",
        description="Redis connection URL"
    )
    redis_db: int = Field(
        default=3,
        env="PREDICTION_REDIS_DB",
        ge=0,
        le=15,
        description="Redis database number"
    )
    redis_password: Optional[str] = Field(
        default=None,
        env="PREDICTION_REDIS_PASSWORD",
        description="Redis password"
    )
    redis_max_connections: int = Field(
        default=20,
        env="PREDICTION_REDIS_MAX_CONNECTIONS",
        ge=1,
        description="Redis max connections"
    )
    
    # Kafka Configuration
    kafka_bootstrap_servers: List[str] = Field(
        default=["localhost:9092"],
        env="PREDICTION_KAFKA_BOOTSTRAP_SERVERS",
        description="Kafka bootstrap servers"
    )
    kafka_topic_prefix: str = Field(
        default="prediction",
        env="PREDICTION_KAFKA_TOPIC_PREFIX",
        description="Kafka topic prefix"
    )
    kafka_consumer_group: str = Field(
        default="prediction_group",
        env="PREDICTION_KAFKA_CONSUMER_GROUP",
        description="Kafka consumer group"
    )
    
    # MLflow Configuration
    mlflow_tracking_uri: str = Field(
        default="./mlruns",
        env="PREDICTION_MLFLOW_TRACKING_URI",
        description="MLflow tracking URI"
    )
    mlflow_experiment_name: str = Field(
        default="vietnamese_stock_prediction",
        env="PREDICTION_MLFLOW_EXPERIMENT_NAME",
        description="MLflow experiment name"
    )
    
    # Logging Configuration
    log_level: LogLevel = Field(
        default=LogLevel.INFO,
        env="PREDICTION_LOG_LEVEL",
        description="Logging level"
    )
    log_json: bool = Field(
        default=True,
        env="PREDICTION_LOG_JSON",
        description="Use JSON logging format"
    )
    log_file: Optional[str] = Field(
        default="logs/prediction_service.log",
        env="PREDICTION_LOG_FILE",
        description="Log file path"
    )
    
    # Rate Limiting
    rate_limit_requests: int = Field(
        default=100,
        env="PREDICTION_RATE_LIMIT_REQUESTS",
        ge=1,
        description="Rate limit requests per window"
    )
    rate_limit_window: int = Field(
        default=60,
        env="PREDICTION_RATE_LIMIT_WINDOW",
        ge=1,
        description="Rate limit window in seconds"
    )
    
    # HTTP Client Configuration
    http_timeout: int = Field(
        default=30,
        env="PREDICTION_HTTP_TIMEOUT",
        ge=1,
        description="HTTP request timeout"
    )
    http_max_connections: int = Field(
        default=100,
        env="PREDICTION_HTTP_MAX_CONNECTIONS",
        ge=1,
        description="HTTP max connections"
    )
    http_retries: int = Field(
        default=3,
        env="PREDICTION_HTTP_RETRIES",
        ge=0,
        description="HTTP retry attempts"
    )
    
    # Circuit Breaker Configuration
    circuit_breaker_failure_threshold: int = Field(
        default=5,
        env="PREDICTION_CIRCUIT_BREAKER_FAILURE_THRESHOLD",
        ge=1,
        description="Circuit breaker failure threshold"
    )
    circuit_breaker_timeout: int = Field(
        default=60,
        env="PREDICTION_CIRCUIT_BREAKER_TIMEOUT",
        ge=1,
        description="Circuit breaker timeout in seconds"
    )
    
    # Monitoring Configuration
    enable_metrics: bool = Field(
        default=True,
        env="PREDICTION_ENABLE_METRICS",
        description="Enable metrics collection"
    )
    metrics_port: int = Field(
        default=9093,
        env="PREDICTION_METRICS_PORT",
        ge=1000,
        le=65535,
        description="Metrics server port"
    )
    
    # CORS Configuration
    allowed_origins: List[str] = Field(
        default=["*"],
        env="PREDICTION_ALLOWED_ORIGINS",
        description="CORS allowed origins"
    )
    allowed_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        env="PREDICTION_ALLOWED_METHODS",
        description="CORS allowed methods"
    )
    allowed_headers: List[str] = Field(
        default=["*"],
        env="PREDICTION_ALLOWED_HEADERS",
        description="CORS allowed headers"
    )
    
    # Feature Flags
    enable_predictions: bool = Field(
        default=True,
        env="PREDICTION_ENABLE_PREDICTIONS",
        description="Enable prediction generation"
    )
    enable_model_training: bool = Field(
        default=True,
        env="PREDICTION_ENABLE_MODEL_TRAINING",
        description="Enable model training"
    )
    enable_auto_retrain: bool = Field(
        default=True,
        env="PREDICTION_ENABLE_AUTO_RETRAIN",
        description="Enable automatic model retraining"
    )
    enable_ensemble: bool = Field(
        default=True,
        env="PREDICTION_ENABLE_ENSEMBLE",
        description="Enable ensemble predictions"
    )
    enable_audit_logging: bool = Field(
        default=True,
        env="PREDICTION_ENABLE_AUDIT_LOGGING",
        description="Enable audit logging"
    )
    enable_performance_logging: bool = Field(
        default=True,
        env="PREDICTION_ENABLE_PERFORMANCE_LOGGING",
        description="Enable performance logging"
    )
    
    # GPU Configuration
    use_gpu: bool = Field(
        default=False,
        env="PREDICTION_USE_GPU",
        description="Enable GPU acceleration"
    )
    gpu_memory_limit: Optional[int] = Field(
        default=None,
        env="PREDICTION_GPU_MEMORY_LIMIT",
        description="GPU memory limit in MB"
    )
    
    # Scheduler Configuration
    retrain_schedule: str = Field(
        default="0 2 * * *",  # Daily at 2 AM
        env="PREDICTION_RETRAIN_SCHEDULE",
        description="Cron schedule for model retraining"
    )
    
    prediction_schedule: str = Field(
        default="*/5 * * * *",  # Every 5 minutes
        env="PREDICTION_PREDICTION_SCHEDULE",
        description="Cron schedule for prediction updates"
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
    
    @validator("ensemble_weights")
    def validate_ensemble_weights(cls, v):
        """Validate ensemble weights sum to 1"""
        total_weight = sum(v.values())
        if abs(total_weight - 1.0) > 0.01:
            raise ValueError(f"Ensemble weights must sum to 1.0, got {total_weight}")
        return v
    
    @validator("target_horizons")
    def validate_target_horizons(cls, v):
        """Validate target horizons are positive"""
        for horizon in v:
            if horizon <= 0:
                raise ValueError(f"Target horizon must be positive, got {horizon}")
        return sorted(v)
    
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
            "predictions": f"{self.kafka_topic_prefix}_predictions",
            "model_updates": f"{self.kafka_topic_prefix}_model_updates",
            "training_status": f"{self.kafka_topic_prefix}_training_status",
            "alerts": f"{self.kafka_topic_prefix}_alerts"
        }
    
    @property
    def redis_keys(self) -> Dict[str, str]:
        """Get Redis key patterns"""
        return {
            "predictions": "pred:predictions:{symbol}:{horizon}",
            "models": "pred:models:{symbol}:{model_type}",
            "features": "pred:features:{symbol}",
            "cache": "pred:cache:{key}"
        }
    
    @property
    def model_paths(self) -> Dict[str, str]:
        """Get model storage paths"""
        return {
            "lstm": f"{self.model_storage_path}/lstm",
            "xgboost": f"{self.model_storage_path}/xgboost",
            "lightgbm": f"{self.model_storage_path}/lightgbm",
            "prophet": f"{self.model_storage_path}/prophet",
            "ensemble": f"{self.model_storage_path}/ensemble"
        }


# Global settings instance
settings = Settings()
