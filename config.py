from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8",)
    secret_key: str

settings = Settings(_env_file=".env")