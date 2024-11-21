from collections.abc import Callable, Coroutine
from typing import Any

from gh_hooks_utils import payloads, validators
from gh_hooks_utils.headers import WebhookHeaders
from pydantic import BaseModel
from sqlmodel import Session

from knowmydevs.app_logger import logger
from knowmydevs.core.config import app_config
from knowmydevs.core.utils import str_utils

type WebhookResponse = Callable[
    [dict[str, Any], Session], Coroutine[type[BaseModel]]
]


async def handle_webhook(
    payload: dict[str, Any], body: bytes, request_details: WebhookHeaders
) -> WebhookResponse:
    event = request_details.x_github_event.lower()

    is_request_valid = validators.is_signature_valid(
        body, app_config.gh_token, request_details.x_hub_signature_256
    )

    if not is_request_valid:
        logger.warning("Received a non valid request")
        pass

    model = _get_model_for_event(event)
    handler = getattr(globals()[f"{event}_service"], "handle")

    return handler, model


def _get_model_for_event(event: str) -> type[BaseModel]:
    event_name_in_pascal = str_utils.snake_to_pascal(event)
    model_name = f"{event_name_in_pascal}Event"

    return getattr(payloads, model_name)
