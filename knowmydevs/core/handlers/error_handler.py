from fastapi import FastAPI

from knowmydevs.core.errors import UnauthorizedError

from .unauthorized_handler import unauthorized_handler


def init_app(app: FastAPI) -> None:
    app.add_exception_handler(
        exc_class_or_status_code=UnauthorizedError,
        handler=unauthorized_handler,  # type: ignore[arg-type]
    )
