import logging

import logfire
from fastapi import FastAPI
from sqlalchemy import Engine

from knowmydevs.core.config import app_config


def init_app(app: FastAPI, engine: Engine | None = None) -> None:
    if app_config.in_observable_environment():
        logfire.configure(token=app_config.logfire_token.get_secret_value())
        logging.basicConfig(handlers=[logfire.LogfireLoggingHandler()])
        logfire.instrument_fastapi(app=app, capture_headers=True)
        logfire.instrument_pydantic()
        logfire.instrument_httpx()
        logfire.instrument_sqlalchemy(engine=engine)
