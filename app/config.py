import os
from pydantic_settings import BaseSettings

# Decide which env file to load
ENV = os.getenv("ENV", "development")  # default = development

class Settings(BaseSettings):
    app_name: str = "YGOLibrary API App"
    debug: bool = False
    database_url: str | None = None
    secret_key : str | None = None

    class Config:
        env_file = f".env.{ENV}"
        env_file_encoding = "utf-8"

settings = Settings()
