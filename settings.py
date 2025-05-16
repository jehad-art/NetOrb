from pydantic import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str
    db_name: str = "network_sec"

    class Config:
        env_file = ".env"

settings = Settings()