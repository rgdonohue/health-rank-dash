# AI-Generated
"""
Application Configuration

Centralized configuration management for HealthRankDash API
using environment variables and default settings.
"""

from functools import lru_cache
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application metadata
    app_name: str = "HealthRankDash API"
    app_version: str = "0.1.0"
    debug: bool = Field(default=False, env="DEBUG")
    
    # API configuration
    api_host: str = Field(default="127.0.0.1", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    max_counties_per_request: int = Field(default=3200, env="MAX_COUNTIES_PER_REQUEST")
    response_timeout_seconds: float = Field(default=30.0, env="RESPONSE_TIMEOUT")
    
    # Data configuration
    data_file_path: str = Field(default="data/analytic_data2025_v2.csv", env="DATA_FILE_PATH")
    indicator_catalog_path: str = Field(default="config/indicator_catalog.json", env="INDICATOR_CATALOG_PATH")
    validation_report_path: str = Field(default="config/validation_report.json", env="VALIDATION_REPORT_PATH")
    
    # Performance settings
    max_response_time_ms: float = Field(default=500.0, env="MAX_RESPONSE_TIME_MS")
    enable_caching: bool = Field(default=True, env="ENABLE_CACHING")
    cache_ttl_seconds: int = Field(default=3600, env="CACHE_TTL_SECONDS")  # 1 hour
    
    # Logging configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # CORS settings
    cors_origins: str = Field(default="http://localhost:3000,http://127.0.0.1:3000", env="CORS_ORIGINS")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    @property
    def cors_origins_list(self) -> list[str]:
        """Convert CORS origins string to list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
        
    @property
    def data_file_path_resolved(self) -> Path:
        """Get resolved path to data file."""
        return Path(self.data_file_path).resolve()
        
    @property
    def indicator_catalog_path_resolved(self) -> Path:
        """Get resolved path to indicator catalog."""
        return Path(self.indicator_catalog_path).resolve()


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()