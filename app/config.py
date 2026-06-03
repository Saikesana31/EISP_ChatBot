"""
app/config.py — centralised settings loaded from environment / .env
                Reads .env file. One Settings class with all config.
                
Used everywhere: from app.config import get_settings
"""

from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache



class Settings(BaseSettings):
    model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            case_sensitive=False,)
    

# Application

# Database
    database_url: str = "postgresql+asyncpg://admin_eips:Praveen%4028@eips-db.postgres.database.azure.com:5432/eips_db"
    database_pool_size: int = 10
    database_max_overflow: int = 20

# Redis/celery

# LLM

# Embeddings

# Alerts

# Langsmith(observability)

# Alert Thresholds


@lru_cache
def get_settings() -> Settings:
    """
    Here we load all the settings from the .env file and cache them.
    This function is used throughout the app to access config values.
    Function is not executed again , it return from cache.
    
    """
    return Settings()