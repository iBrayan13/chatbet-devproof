from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    CHATBET_BASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")