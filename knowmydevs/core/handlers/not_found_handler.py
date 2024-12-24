from fastapi import Request, status
from fastapi.responses import JSONResponse

from knowmydevs.app_logger import logger
from knowmydevs.core.errors import NotFoundError


async def not_found_handler(
    request: Request, not_found_err: NotFoundError
) -> None:
    logger.warning(f"HTTP 404 Not Found error was caught: {not_found_err}")

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(not_found_err)},
    )
