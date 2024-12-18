import base64
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from knowmydevs.app_logger import logger
from knowmydevs.core.errors import UnauthorizedError

from .kms import get_public_key

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/oauth2/token")


def get_current_installation(
    authorization: Annotated[str, Depends(oauth2_scheme)],
) -> int:
    pub_key = get_public_key()

    try:
        jwt_token = jwt.decode(
            jwt=authorization,
            key=pub_key,
            algorithms=["RS256"],
            options={"verify_signature": True},
        )

    except jwt.ExpiredSignatureError as exp_err:
        logger.warning(f"Expired token: {exp_err}")

        raise UnauthorizedError("Expired token")

    return int(jwt_token.get("username"))


def jwtfy(value: str | bytes) -> str:
    if isinstance(value, str):
        val = value.encode()
    elif isinstance(value, bytes):
        val = value
    else:
        raise ValueError("Value must be a string or a bytes")

    return base64.urlsafe_b64encode(val).decode().rstrip("=")
