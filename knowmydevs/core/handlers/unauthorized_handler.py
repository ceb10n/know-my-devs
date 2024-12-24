from fastapi import Request, status
from fastapi.responses import JSONResponse

from knowmydevs.app_logger import logger
from knowmydevs.core.errors import UnauthorizedError


async def unauthorized_handler(
    request: Request, unauthorized_err: UnauthorizedError
) -> None:
    logger.warning(f"HTTP 401 Unauthorized error was caught: {unauthorized_err}")

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(unauthorized_err)},
        headers={"WWW-Authenticate": "Bearer"},
    )