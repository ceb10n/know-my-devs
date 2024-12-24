from fastapi import Request, status
from fastapi.responses import JSONResponse

from knowmydevs.app_logger import logger
from knowmydevs.core.errors import InternalError


async def internal_error_handler(
    request: Request, internal_err: InternalError
) -> None:
    logger.warning(f"HTTP 500 Internal Server Error was caught: {internal_err}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(internal_err)},
    )
