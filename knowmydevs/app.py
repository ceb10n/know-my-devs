import datetime

from fastapi import FastAPI

from knowmydevs import logger
from knowmydevs.core.config import app_config
from knowmydevs.core.infra.events.fastapi_lifespan import lifespan


def create_app() -> FastAPI:
    logger.info(
        f"Starting {app_config.app_name} at {datetime.datetime.now(datetime.UTC)}"
    )
    app = FastAPI(lifespan=lifespan)

    return app
