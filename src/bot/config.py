from pydantic_settings import BaseSettings
from pathlib import Path


class Config(BaseSettings):
    BOT_TOKEN: str
    API_URL: str

    class Config:
        env_file = Path(__file__).parent.parents[1] / ".env"
        extra = "allow"


config = Config()
