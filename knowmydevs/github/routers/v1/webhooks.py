from typing import Annotated, Any

from fastapi import APIRouter, BackgroundTasks, Header, Request
from gh_hooks_utils.headers import WebhookHeaders

from knowmydevs.github.services.webhooks import webhook_service

router = APIRouter()


@router.post("/webhooks")
async def handle_webhook(
    request: Request,
    payload: dict[str, Any],
    headers: Annotated[WebhookHeaders, Header()],
    background_tasks: BackgroundTasks,
):
    body = await request.body()
    handler, model = webhook_service.handle_webhook(payload, body, headers)

    background_tasks.add_task(handler, model, session)
