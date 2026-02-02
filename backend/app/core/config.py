from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database
    database_path: str = "/app/data/skills.db"
    database_encryption_key: str

    # API Keys
    github_token: Optional[str] = None
    npm_token: Optional[str] = None

    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Redis
    redis_url: str = "redis://redis:6379/0"

    # CORS
    frontend_url: str = "http://localhost:3000"

    # Scraping Schedule
    github_scrape_interval_minutes: int = 60
    npm_scrape_interval_hours: int = 24
    pypi_scrape_interval_hours: int = 24
    huggingface_scrape_interval_minutes: int = 60

    # Rate Limiting
    rate_limit_per_minute: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
