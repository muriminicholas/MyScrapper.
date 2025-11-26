# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    APP_NAME: str = "ScrapyFlow"
    SECRET_KEY: str = "change-me-to-a-very-strong-random-string-in-production"  # openssl rand -hex 32
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/scrapyflow"

    # Redis (for RQ + WebSocket pub/sub)
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security
    ALLOWED_HOSTS: list[str] = ["*"]

    # Scraping
    DEFAULT_TIMEOUT: int = 60
    MAX_CONCURRENT_TASKS_PER_USER: int = 10

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()