import datetime

from fastapi import FastAPI

from knowmydevs import logger, version
from knowmydevs.auth.routers import routers as auth_routers
from knowmydevs.core.config import app_config
from knowmydevs.core.handlers import error_handler
from knowmydevs.core.infra.db import postgres
from knowmydevs.core.infra.events.fastapi_lifespan import lifespan
from knowmydevs.core.observability import logfire_app
from knowmydevs.github.routers import routers as github_routers


def create_app() -> FastAPI:
    logger.info(
        f"Starting {app_config.app_name} at {datetime.datetime.now(datetime.UTC)}"
    )
    app = FastAPI(
        lifespan=lifespan,
        title="Know My Devs",
        summary="Github App to generate summary of PRs and Discussions",
        version=version.VERSION,
        contact={
            "name": "Rafael de Oliveira Marques",
            "url": "https://github.com/ceb10n",
            "email": "rafaelomarques@gmail.com"
        },
        license_info={
            "name": "MIT License",
            "identifier": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    )   
    error_handler.init_app(app)
    engine = postgres.init_app()
    logfire_app.init_app(app, engine=engine)
    app.include_router(auth_routers.router)
    app.include_router(github_routers.router)

    return app
