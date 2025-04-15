# app/core/config.py
from pydantic import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings."""
    app_name: str = "Event Manager API"
    debug: bool = False
    max_login_attempts: int = 5
    
    # Add any other configuration settings here
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    """Get application settings."""
    return Settings()