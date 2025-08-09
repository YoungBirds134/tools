from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    """Application configuration."""

    app_name: str = Field(default="Master Data Service", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    debug: bool = Field(default=False, description="Enable debug mode")

    allowed_origins: List[str] = Field(default=["*"], description="Allowed CORS origins")
    allowed_methods: List[str] = Field(default=["*"], description="Allowed HTTP methods")
    allowed_headers: List[str] = Field(default=["*"], description="Allowed headers")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
