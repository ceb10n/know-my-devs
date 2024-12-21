import datetime
import json
import uuid

from knowmydevs.app_logger import logger
from knowmydevs.auth.payloads import TokenCredential, TokenForm
from knowmydevs.auth.responses import TokenResponse
from knowmydevs.core.auth import cognito, kms
from knowmydevs.core.auth.token import jwtfy
from knowmydevs.core.errors import UnauthorizedError

header = jwtfy(json.dumps({"alg": "RS256", "typ": "JWT", "kid": "knowmydevs"}))


async def issue_token(
    credential: TokenCredential, form: TokenForm
) -> TokenResponse:
    logger.info(f"Authenticating installation {credential.username}")
    app_client = cognito.find_app_client(credential.username)

    if not app_client:
        raise UnauthorizedError("Invalid credentials")

    _ = await cognito.client_credentials_auth(
        credential.username, credential.password
    )

    exp = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=3600)
    logger.debug(f"Expiration set to {exp}")

    jwt_payload = {
        "iss": "knowmydevs",
        "iat": int(datetime.datetime.now(datetime.UTC).timestamp()),
        "exp": int(exp.timestamp()),
        "jti": str(uuid.uuid4()),
        "username": app_client.client_name,
    }

    payload = jwtfy(json.dumps(jwt_payload))

    message = f"{header}.{payload}"
    logger.debug("Signing token")
    signature = kms.sign_token(message)

    jwt_signture = jwtfy(signature)

    token = f"{header}.{payload}.{jwt_signture}"

    return TokenResponse(access_token=token, expires_in=3600)
