"""
Feature: Core Configuration
File Purpose: Load application settings from environment variables
Owner: Misha
Dependencies: backend/.env
Last Updated: 2026-03-14
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TravelMind Backend"
    app_env: str = "development"
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000
    database_url: str
    google_maps_api_key: str = ""
    llm_api_key: str = ""

    model_config = SettingsConfigDict(env_file="backend/.env", env_file_encoding="utf-8")


settings = Settings()
