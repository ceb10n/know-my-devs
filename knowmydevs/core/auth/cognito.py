import boto3

from knowmydevs.core.config import app_config


def create_app_client(installation_id: int) -> str:
    client = boto3.client("cognito-idp", region_name=app_config.aws_region)

    r = client.create_user_pool_client(
        UserPoolId=app_config.aws_cognito_pool_id,
        ClientName=str(installation_id),
        GenerateSecret=True,
    )

    return r.get("UserPoolClient", {}).get("ClientSecret")
