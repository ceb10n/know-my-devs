from functools import lru_cache

import boto3
from botocore.exceptions import ClientError
from cryptography.hazmat.primitives import serialization

from knowmydevs.app_logger import logger
from knowmydevs.core.config import app_config
from knowmydevs.core.errors import InternalError


def sign_token(token: str) -> bytes:
    client = _get_kms_client()

    r = client.sign(
        KeyId=app_config.aws_kms_key_arn,
        Message=token.encode(),
        MessageType="RAW",
        SigningAlgorithm=app_config.aws_kms_alg,
    )

    return r.get("Signature")


def get_public_key() -> bytes:
    client = _get_kms_client()

    try:
        logger.debug("Getting kms public key")
        r = client.get_public_key(KeyId=app_config.aws_kms_key_arn)

    except ClientError as cli_err:
        err_code = cli_err.response["Error"]["Code"]
        err_msg = ["Error"]["Message"]
        logger.warning(f"Error getting kms public key: {err_code} - {err_msg}")

        raise InternalError("An internal error occurred. Sorry, it's on us.")

    logger.debug("Loading der public key")
    der_public_key = serialization.load_der_public_key(r.get("PublicKey"))

    logger.debug("Getting public bytes from the key")
    return der_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


@lru_cache
def _get_kms_client():
    if not app_config.aws_region:
        raise ValueError("AWS Region is required")

    try:
        logger.debug(
            f"Starting new boto3 session for region {app_config.aws_region}"
        )
        session = boto3.session.Session(region_name=app_config.aws_region)

        return session.client("kms")

    except ClientError as cli_err:
        err_code = cli_err.response["Error"]["Code"]
        err_msg = ["Error"]["Message"]

        logger.warning(f"Error creating kms client: {err_code} - {err_msg}")
