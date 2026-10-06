import logging
from collections.abc import Generator
from functools import lru_cache

from pydantic import BaseSettings, Field, SecretStr
from sqlmodel import Engine, Session, create_engine

DEFAULT_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/fast_api_monolith_example"
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"


@lru_cache
def get_db_engine() -> Engine:
    return create_engine(get_settings().database_url)


def get_db_session() -> Generator[Session]:
    with get_db_engine() as session:
        yield session


class Settings(BaseSettings):
    database_url: str = DEFAULT_DATABASE_URL
    debug: bool = False
    jwt_secret_key: SecretStr = Field(min_length=32)


def configure_logging(*, debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format=LOG_FORMAT)


@lru_cache
def get_settings() -> Settings:
    return Settings()
