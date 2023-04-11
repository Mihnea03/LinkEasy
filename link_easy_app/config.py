from pydantic import BaseSettings


class Settings(BaseSettings):
    env_name : str = "Development"
    base_url : str = "http://localhost:8080"
    db_url : str = "sqlite:///./shortener.db"

def get_settings() -> Settings:
    settings = Settings()

    return settings