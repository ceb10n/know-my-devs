from fastapi import HTTPException, Request, status

from knowmydevs.app_logger import logger
from knowmydevs.core.errors import UnauthorizedError


async def unauthorized_handler(
    request: Request, unauthorized_err: UnauthorizedError
) -> None:
    logger.warning(f"HTTP 401 Unauthorized error was caught: {unauthorized_err}")

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=str(unauthorized_err),
        headers={"WWW-Authenticate": "Bearer"},
    )
