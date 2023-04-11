from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    env_name : str
    base_url : str
    db_url : str

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings