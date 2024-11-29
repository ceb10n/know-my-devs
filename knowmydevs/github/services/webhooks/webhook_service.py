import importlib
from collections.abc import Callable, Coroutine
from typing import Any

import logfire
from gh_hooks_utils import payloads, validators
from gh_hooks_utils.headers import WebhookHeaders
from pydantic import BaseModel
from sqlmodel import Session

from knowmydevs.app_logger import logger
from knowmydevs.core.config import app_config
from knowmydevs.core.errors import BadRequestError
from knowmydevs.core.utils import str_utils

type WebhookResponse = Callable[
    [type[BaseModel], Session], Coroutine[type[BaseModel]]
]


async def handle_webhook(
    payload: dict[str, Any],
    body: bytes,
    request_details: WebhookHeaders,
    session: Session,
) -> WebhookResponse:
    logger.info(f"Received payload -> {payload}")

    with logfire.span("Github Webhook Event"):
        event = request_details.x_github_event.lower()
        is_request_valid = True

        # remove the validation for local environment to make
        # local testing easier
        if not app_config.is_local_environment():
            is_request_valid = validators.is_signature_valid(
                body,
                app_config.gh_token.get_secret_value(),
                request_details.x_hub_signature_256,
            )

        if not is_request_valid:
            logger.warning(
                f"Received an invalid request. Signature {request_details.x_hub_signature_256}"
            )
            raise BadRequestError("Invalid payload")

        model = _get_model_for_event(event, payload)
        module = importlib.import_module(
            f"knowmydevs.github.services.webhooks.{event}_service"
        )
        handler = getattr(module, "handle")

        await handler(model, session)


def _get_model_for_event(
    event: str, payload: dict[str, Any]
) -> type[BaseModel]:
    event_name_in_pascal = str_utils.snake_to_pascal(event)
    model_name = f"{event_name_in_pascal}Event"

    return getattr(payloads, model_name)(**payload)
