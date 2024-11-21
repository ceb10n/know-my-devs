from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import URL
from sqlmodel import SQLModel

from knowmydevs.core.config import app_config

_engine: Engine | None


def get_engine() -> Engine:
    global _engine

    if _engine:
        return _engine
    
    raise Exception("Engine not initialized")


def init_app():
    global _engine

    url = URL.create(
        drivername="postgresql",
        username=app_config.pg_username,
        password=app_config.pg_password.get_secret_value(),
        host=app_config.pg_host,
        database=app_config.pg_database,
    )

    _engine = create_engine(url)

    if app_config.is_local_environment():
        SQLModel.metadata.create_all(_engine)
