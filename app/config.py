from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    APP_ENV: str

    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_USER: str | None = Field(default=None)
    ELASTICSEARCH_PASSWORD: str | None = Field(default=None)


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
