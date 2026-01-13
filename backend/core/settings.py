from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ACCESS_TOKEN_COOKIE_NAME: str = "notion_agent_token"

    model_config = ConfigDict(extra="ignore", env_file=".env")

settings = Settings()
