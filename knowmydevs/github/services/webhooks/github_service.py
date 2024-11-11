import hashlib
import hmac
from typing import Any

from knowmydevs.core.config import app_config


def is_signature_valid(gh_payload: dict[str, Any], signature: str) -> bool:
    hash_object = hmac.new(
        app_config.gh_token.encode("utf-8"),
        msg=gh_payload,
        digestmod=hashlib.sha256,
    )

    expected_signature = "sha256=" + hash_object.hexdigest()

    return hmac.compare_digest(expected_signature, signature)
