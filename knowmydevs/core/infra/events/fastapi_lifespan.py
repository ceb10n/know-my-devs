from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from knowmydevs.app_logger import logger
from knowmydevs.core.observability import sentry


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("-> Lifespan start")
    sentry.init_app()

    yield