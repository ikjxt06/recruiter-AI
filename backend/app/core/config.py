from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "TalentIQ AI"
    environment: str = "development"
    secret_key: str
    access_token_expire_minutes: int = 720
    database_url: str
    chroma_path: str = "./.chroma"
    upload_dir: str = "./uploads"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-1.5-flash"
    allowed_origins: str = "http://localhost:5173"

    @property
    def upload_path(self) -> Path:
        path = Path(self.upload_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
