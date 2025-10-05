"""
Configuration management for AI Audio Listener.
"""

import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False

    # Redis settings
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None

    # Audio processing settings
    audio_sample_rate: int = 16000
    audio_channels: int = 1
    audio_chunk_size: int = 1024

    # WebSocket settings
    websocket_ping_interval: int = 20
    websocket_ping_timeout: int = 10

    # AI settings
    openai_api_key: Optional[str] = None
    whisper_model: str = "base"

    # Logging settings
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
