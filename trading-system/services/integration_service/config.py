"""
Configuration settings for SSI Integration Service
"""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid"
    )
    
    # Application settings
    app_name: str = Field(default="SSI Integration Service", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="development", description="Environment")
    
    # Server settings
    host: str = Field(default="0.0.0.0", description="Host to bind")
    port: int = Field(default=8000, description="Port to bind")
    workers: int = Field(default=1, description="Number of workers")
    
    # Redis settings
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_db: int = Field(default=0, description="Redis database")
    redis_password: Optional[str] = Field(default=None, description="Redis password")
    redis_ssl: bool = Field(default=False, description="Redis SSL")
    redis_timeout: int = Field(default=30, description="Redis timeout in seconds")
    
    # Cache TTL settings (in seconds)
    cache_ttl_token: int = Field(default=3600, description="Token cache TTL")
    cache_ttl_master_data: int = Field(default=86400, description="Master data cache TTL")
    cache_ttl_market_data: int = Field(default=300, description="Market data cache TTL")
    
    # SSI API FCData Credentials 
    consumer_id_fc_data: str = Field(default="9db5f2ee570f4624a7e9e08d408c663a", description="SSI Consumer ID")
    consumer_secret_fc_data: str = Field(default="e42fd610cdc14636bc28e17b1c8aa949", description="SSI Consumer Secret")
    private_key_fc_data: str = Field(
        default="PFJTQUtleVZhbHVlPjxNb2R1bHVzPndHSHlqNmc1MTJHU2l6anZQa2IxNGxwMDBmMlkrZ3FkWHU5eHdEemRDWHNHRXEwWTdEMVVoN29uUG5jWmRpczlldEY0Sm9scGxoaW54MWNwOHNGcXZqeitKWG80M2tPazJWcW5YdXpJc1c1TU1MOERMMjBUMlliQUJqT01qWGRtNWxab1F6ZmFBQmVZYkNLODRuQmhoVW9MSXFPQnladHF0ZFBvWnJpRXVzcz08L01vZHVsdXM+PEV4cG9uZW50PkFRQUI8L0V4cG9uZW50PjxQPi9rMDA4ZnhBTlc3NDFQajJnWVBTeStlL25RbTc1ZWtrcWZMaVZxWUZVdmRkb3RyVDRzaHNnOFh6Q2d6a2NPdDI5V21IN2tzTVI2YlA4WlZTTlE1QU9RPT08L1A+PFE+d2FyZjNFVlphbHk3L2VVWkFPU0RER1FmdEM1dFFWdUV3OHNuOHFYZnZhSDlOczJFekhCZVE3QWFnWmJYb3YwT1U4dkdoTHR4WGQyVmd6Q3BPa3VMSXc9PTwvUT48RFA+bFNWcENRZStETml4L2c2cVhObVl0MWlMYkNuNlZ1Ui9TV0dYVitSMU9PeTFzVDhRaUhDdUhEYnJ6UmcwbnZtcXdsS0xrN25XVU92SUI5Tmc3SmNZR1E9PTwvRFA+PERRPmdKV3NabnFoQUk2cnZzcHlqSFlzVUhqVjEvTVBWVnFuVHJ3L1BNdEhQNGdqTUZUS1BGYkxMNVBvTld4cXBldndyRkJhOFZ2bXpGVEg1VC9VekVER0V3PT08L0RRPjxJbnZlcnNlUT5uNVBtaEFaNlBWenhRdVlLZmYwYkN3SGo0Y3VaaEZUMXc0eUNDbWVTQWM1V2RNV3J0V3BMUHpzU1ZJeE9FYmVQWWtmTzhJQVhDbW5XdVFGSXdEUHUyZz09PC9JbnZlcnNlUT48RD5zZURlbWgxOWZidmw5M3hwR1RnYldYTXgySWVXem5yS0QyRnQxOFZ1eXJsSllETlVlL29wRW1YNHF6VU1BY3J4U1lJc2lkVThIMkFrb1pmaVhXYWcvaTdMVU5id0JqTkpMeEd0L1JQcWpFUWhmeWo1TTQrUWhuUlk5VWdmQ0pZbEx2ZmxxMEV4YlUzdXVXOFQvZmc2bU5vczI4a0g5N0FoaCthdXVHd3Ftc0U9PC9EPjwvUlNBS2V5VmFsdWU+",
        description="SSI Private Key (Base64)"
    )
    public_key_fc_data: str = Field(
        default="PFJTQUtleVZhbHVlPjxNb2R1bHVzPndHSHlqNmc1MTJHU2l6anZQa2IxNGxwMDBmMlkrZ3FkWHU5eHdEemRDWHNHRXEwWTdEMVVoN29uUG5jWmRpczlldEY0Sm9scGxoaW54MWNwOHNGcXZqeitKWG80M2tPazJWcW5YdXpJc1c1TU1MOERMMjBUMlliQUJqT01qWGRtNWxab1F6ZmFBQmVZYkNLODRuQmhoVW9MSXFPQnladHF0ZFBvWnJpRXVzcz08L01vZHVsdXM+PEV4cG9uZW50PkFRQUI8L0V4cG9uZW50PjwvUlNBS2V5VmFsdWU+",
        description="SSI Public Key (Base64)"
    )
        
    # SSI API FCTrading Credentials 
    consumer_id_fc_trading: str = Field(default="9db5f2ee570f4624a7e9e08d408c663a", description="SSI Consumer ID")
    consumer_secret_fc_trading: str = Field(default="8356e0ffe4ff400d937c6171faa61b56", description="SSI Consumer Secret")
    account: str = Field(default="Q023951", description="Trading account")
    fc_trading_access_token: Optional[str] = Field(default=None, description="FC Trading Access Token - managed via Redis cache")
    private_key_fc_trading: str = Field(
        default="PFJTQUtleVZhbHVlPjxNb2R1bHVzPjVzZmVKUDhudm8wYUlkcktjVkJHOTlGVnpJTG9lNXZOR0dxQXNJaWdQZi9yUmUwZWRXQTNhNjhwSUQ1b3M3SkY5bThzZTAvNmhGMkdaOC9oZ082MGdHdDVBU25EWlp5WFVNTGVmUmltZEJLUHZuNlBscEpOR0NTK2orc0tvU21MMW44OTZ1NFZoVVEzVnkvT0p6djhQMWNaeUtDL1ozWDB1RFROWTdGRU5WVT08L01vZHVsdXM+PEV4cG9uZW50PkFRQUI8L0V4cG9uZW50PjxQPitrVDVLMXdmRUVLeEIreWt1a2s2MENQQ3hDc2N1bGxPZ1FjSzYzMERmeFZrRWFyejdxeDIwVnZnWUF4Wi9xa256WTBVTEJTR1YycUZUU1lWUXE0WkxRPT08L1A+PFE+N0JDbjQ0ejQrWlRObVUzYWRQRzYzNjhmc01LM3lxVkxaMmpKU3ZWR2pwNkdmQWNwU0YxbS9BOE90bHVNNFcvVitjRDQ3STY2aTZWM3ZQZ1BiaURWeVE9PTwvUT48RFA+TzlNVkJPcG1lb3FXcXVCRW1FczlCZGdtaktJSm9mb0xMQWkwOFluV3RpQTA1WXhKOXptK3hWa0REN0trS0ozaTU5M2JmcFlCYnhBRmdXV2pHMmRtbVE9PTwvRFA+PERRPlFjQko0dm1MQjRsSTB1QjZib1E5OXJ2Q2FldHlZY0UwaFhNTVRoS1BPbjR4R3k2cmN2cUJDc2Z1NHlBUTEySGRDWm1VTzk5dFdpUVdlODNrRGxxYThRPT08L0RRPjxJbnZlcnNlUT5LUU1VZEJyNmxRV2NacnkwQjJWMWI0dXZyMlFuVFNLU1N5N2xWdGdKWGhycEJlNEwrNlZielVvdFZmOUdQZmlKcVliY0pCT1lSdDM5QWtRcTg5amxQUT09PC9JbnZlcnNlUT48RD5mOWNYNThhd2JZNGNlOFNIZ0YzSDhsK3o5NlpNd3F4NzRKcWV6eXZnR0hnOERIQmQvd2RkcS9sTC91Q1RmM2V4NmVHTDhvTkxjeWViM01YN1ZUOWdJUFgvc3EwdFlPdDU5eDFMaXN4VEQ2QUNucUYzU2RlMU01aVV4TVkxM1lzL0FTUzlIU2ZZL051Q1AraFNERFRhbnViWkpQa3hIdTBnWjg0dFpla0xEZ0U9PC9EPjwvUlNBS2V5VmFsdWU+",
        description="SSI Private Key (Base64)"
    )
    public_key_fc_trading: str = Field(
        default="PFJTQUtleVZhbHVlPjxNb2R1bHVzPjVzZmVKUDhudm8wYUlkcktjVkJHOTlGVnpJTG9lNXZOR0dxQXNJaWdQZi9yUmUwZWRXQTNhNjhwSUQ1b3M3SkY5bThzZTAvNmhGMkdaOC9oZ082MGdHdDVBU25EWlp5WFVNTGVmUmltZEJLUHZuNlBscEpOR0NTK2orc0tvU21MMW44OTZ1NFZoVVEzVnkvT0p6djhQMWNaeUtDL1ozWDB1RFROWTdGRU5WVT08L01vZHVsdXM+PEV4cG9uZW50PkFRQUI8L0V4cG9uZW50PjwvUlNBS2V5VmFsdWU+",
        description="SSI Public Key (Base64)"
    )
    
    # SSI API URLs
    fc_data_url: str = Field(default="https://fc-data.ssi.com.vn/", description="FC Data API URL")
    fc_data_stream_url: str = Field(default="https://fc-datahub.ssi.com.vn/", description="FC Data Stream URL")
    fc_trading_url: str = Field(default="https://fc-tradeapi.ssi.com.vn/", description="FC Trading API URL")
    fc_trading_stream_url: str = Field(default="https://fc-tradehub.ssi.com.vn/", description="FC Trading Stream URL")
    
    # API Rate limiting
    rate_limit_requests: int = Field(default=100, description="Rate limit requests per minute")
    rate_limit_window: int = Field(default=60, description="Rate limit window in seconds")
    
    # Timeout settings
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    connection_timeout: int = Field(default=10, description="Connection timeout in seconds")
    
    # Retry settings
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    retry_delay: float = Field(default=1.0, description="Retry delay in seconds")
    
    # Logging
    log_level: str = Field(default="INFO", description="Log level")
    log_format: str = Field(default="json", description="Log format")
    
    @property
    def redis_url(self) -> str:
        """Build Redis URL from components"""
        auth = f":{self.redis_password}@" if self.redis_password else ""
        protocol = "rediss" if self.redis_ssl else "redis"
        return f"{protocol}://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"


# Global settings instance
settings = Settings()
