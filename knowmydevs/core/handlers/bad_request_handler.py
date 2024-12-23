from fastapi import Request, status
from fastapi.responses import JSONResponse

from knowmydevs.app_logger import logger
from knowmydevs.core.errors import BadRequestError


async def bad_request_handler(
    request: Request, bad_request_err: BadRequestError
) -> None:
    logger.warning(f"HTTP 400 Bad Request error was caught: {bad_request_err}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(bad_request_err)},
    )
