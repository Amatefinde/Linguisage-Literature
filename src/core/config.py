import os
from os.path import join
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

    api_v1_prefix: str = "/api/v1"

    base_dir: Path = BASE_DIR
    static_path: str
    abs_static_path: str = join(BASE_DIR, os.environ.get("STATIC_PATH"))
    epub_dir: str = join(abs_static_path, "epubs")
    fb2_tmp: str = join(abs_static_path, "fb2_tmp")
    epub_cover_dir: str = join(abs_static_path, "epub_covers")

    base_url: str
    REDIS_HOST: str


settings = Settings()

if __name__ == "__main__":
    print(*settings.__dict__.items(), sep="\n")
