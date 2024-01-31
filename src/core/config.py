import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    # Database connection
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    db_echo: bool = False

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    base_dir: Path = BASE_DIR

    api_v1_prefix: str = "/api/v1"


settings = Settings()

if __name__ == "__main__":
    print(*settings.__dict__.items(), sep="\n")
