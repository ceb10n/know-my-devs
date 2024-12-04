from collections.abc import Iterable

from sqlalchemy import Engine
from sqlalchemy.engine import URL
from sqlmodel import Session, SQLModel, create_engine

from knowmydevs.app_logger import logger
from knowmydevs.core.config import app_config

_engine: Engine | None


def get_session() -> Iterable[Session]:
    global _engine

    if _engine:
        yield Session(_engine)
    else:
        raise Exception("Engine is not initialized")


def init_app() -> None:
    logger.info("Initializing postgres connection")
    global _engine

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=app_config.pg_username,
        password=app_config.pg_password.get_secret_value(),
        host=app_config.pg_host,
        database=app_config.pg_database,
    )

    _engine = create_engine(url)

    if app_config.is_local_environment():
        logger.info("Creating databases in local environment")
        SQLModel.metadata.create_all(_engine)

    logger.info("Database intialized")
