from collections.abc import Callable, Coroutine
from typing import Any

from pydantic import BaseModel
from sqlmodel import Session

from knowmydevs.app_logger import logger
from knowmydevs.github.schemas.webhooks.github import WebhookHeaders
from knowmydevs.github.services.webhooks import github_service

type WebhookResponse = Callable[
    [dict[str, Any], Session], Coroutine[type[BaseModel]]
]


async def handle_webhook(
    payload: dict[str, Any], request_details: WebhookHeaders
) -> WebhookResponse:
    is_request_valid = github_service.is_signature_valid(
        payload, request_details.x_hub_signature_256
    )

    if not is_request_valid:
        logger.warning("Received a non valid request")
        pass

    return getattr(
        globals()[f"{request_details.x_github_event}_service"], "handle"
    )
