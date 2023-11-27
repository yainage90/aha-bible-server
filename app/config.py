from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    APP_ENV: str

    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_USER: str | None = Field(default=None)
    ELASTICSEARCH_PASSWORD: str | None = Field(default=None)


"""
class DevelopmentSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.development")


class ProductionSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env")
"""


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
