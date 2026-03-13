from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # App
    APP_NAME: str = "TravelMind AI"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str

    # AI / LLM
    OPENAI_API_KEY: str | None = None

    # Google Maps
    GOOGLE_MAPS_API_KEY: str | None = None

    # Security
    SECRET_KEY: str = "supersecret"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Returns cached settings object."""
    return Settings()


settings = get_settings()