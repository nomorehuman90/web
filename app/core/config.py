from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    SECRET_KEY: str
    ALGORITHM: str
    DATABASE_URL: str
    KAKAO_REST_API_KEY: str
    KAKAO_CLIENT_SECRET: str
    KAKAO_REDIRECT_URI: str
    PORTONE_API_SECRET: str = ""


settings = Settings()
