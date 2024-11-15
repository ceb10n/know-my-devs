from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from knowmydevs.core.infra.db import postgres
from knowmydevs.core.observability import logfire_app, sentry


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    postgres.init_app()
    logfire_app.init_app()
    sentry.init_app()

    yield