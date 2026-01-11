from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    NOTION_API_KEY: str
    OPENAI_API_KEY: str
    OPENAI_MODEL_PLANNER: str = "gpt-4o-mini"
    OPENAI_MODEL_ANSWER: str = "gpt-4o"
    MAX_TURNS: int = 10

    model_config = ConfigDict(extra="ignore", env_file=".env")

settings = Settings()
