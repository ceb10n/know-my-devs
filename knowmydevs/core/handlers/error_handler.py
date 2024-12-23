from fastapi import FastAPI

from knowmydevs.core.errors import (
    BadRequestError,
    InternalError,
    UnauthorizedError,
)

from .bad_request_handler import bad_request_handler
from .internal_error_handler import internal_error_handler
from .unauthorized_handler import unauthorized_handler


def init_app(app: FastAPI) -> None:
    app.add_exception_handler(
        exc_class_or_status_code=BadRequestError,
        handler=bad_request_handler,  # type: ignore[arg-type]
    )

    app.add_exception_handler(
        exc_class_or_status_code=InternalError,
        handler=internal_error_handler,  # type: ignore[arg-type]
    )

    app.add_exception_handler(
        exc_class_or_status_code=UnauthorizedError,
        handler=unauthorized_handler,  # type: ignore[arg-type]
    )
