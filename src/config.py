
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.config import Config

#Pydantic Settings help you manage configuration variables (like API keys, database URLs,
#or environment variables) in a structured and easy way.

#SettingsConfigDict controls how your settings class works in Pydantic v2, making it easier
#to load, validate, and manage environment variables.

class Settings(BaseSettings):
    DATABASE_URL:str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

Config=Settings()