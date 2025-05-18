from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str
    db_name: str = "network_sec"
    agent_token: str

    class Config:
        env_file = ".env"

settings = Settings()