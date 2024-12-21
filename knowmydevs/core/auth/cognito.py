import boto3
import httpx
import logfire
from botocore.exceptions import ClientError

from knowmydevs.app_logger import logger
from knowmydevs.core.config import app_config

from .models import AppClient, Token


async def client_credentials_auth(
    client_id: str, client_secret: str
) -> Token | None:
    auth = httpx.BasicAuth(username=client_id, password=client_secret)
    data = {"grant_type": "client_credentials"}
    async with httpx.AsyncClient() as client:
        r = await client.post(
            app_config.aws_cognito_token_url, auth=auth, data=data
        )

        logger.debug(r.json())

        return Token(**r.json())


def find_app_client(client_id: str) -> AppClient | None:
    logger.debug(f"Looking for app client {client_id}")

    with logfire.span("Find App Client") as span:
        client = boto3.client("cognito-idp", region_name=app_config.aws_region)

        try:
            r = client.describe_user_pool_client(
                UserPoolId=app_config.aws_cognito_pool_id,
                ClientId=client_id,
            )

            return AppClient(**r.get("UserPoolClient", {}))

        except ClientError as client_err:
            logger.warning(f"Error looking for app client: {client_err}")
            span.record_exception(client_err)

        return None


def create_app_client(installation_id: int) -> AppClient | None:
    logger.debug(f"Creating app client for installation {installation_id}")

    with logfire.span("Creating App Client") as span:
        client = boto3.client("cognito-idp", region_name=app_config.aws_region)

        try:
            r = client.create_user_pool_client(
                UserPoolId=app_config.aws_cognito_pool_id,
                ClientName=str(installation_id),
                GenerateSecret=True,
                AllowedOAuthFlows=["client_credentials"],
                AllowedOAuthScopes=["default-m2m-resource-server-ayrlxg/read"],
                AllowedOAuthFlowsUserPoolClient=True,
            )

            return AppClient(**r.get("UserPoolClient", {}))

        except ClientError as client_err:
            logger.warning(f"Error creating app client: {client_err}")
            span.record_exception(client_err)

        return None
