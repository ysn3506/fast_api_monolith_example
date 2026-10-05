from functools import lru_cache

from pydantic import Field, SecretStr
from sqlmodel import Engine, Session, create_engine

DEFAULT_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/fast_api_monolith_example"
LOG_MODEL =  "%(asctime)s %(levelname)s %(name)s %(message)s"



@lru_cache
def get_db_engine() -> Engine:
    return create_engine(DEFAULT_DATABASE_URL)

def get_db_session() -> Session:
    with get_db_engine() as engine:
        return Session(engine)



class Settings:
    database_url: str = DEFAULT_DATABASE_URL
    debug:bool=False
    jwt:SecretStr=Field(min_length=32)

    