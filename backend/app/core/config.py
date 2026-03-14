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
    routing_base_url: str = "https://router.project-osrm.org"
    ai_service_base_url: str = "http://127.0.0.1:8001"
    ai_service_timeout_seconds: float = 120.0
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    jwt_secret: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_exp_minutes: int = 720

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
