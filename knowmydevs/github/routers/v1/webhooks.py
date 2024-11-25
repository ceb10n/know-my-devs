from typing import Annotated, Any

from fastapi import APIRouter, BackgroundTasks, Depends, Header, Request
from gh_hooks_utils.headers import WebhookHeaders
from sqlmodel import Session

from knowmydevs.core.infra.db import get_session
from knowmydevs.github.services.webhooks import webhook_service

router = APIRouter()


@router.post("/webhooks")
async def handle_webhook(
    request: Request,
    payload: dict[str, Any],
    background_tasks: BackgroundTasks,
    headers: Annotated[WebhookHeaders, Header()],
    session: Session = Depends(get_session)
):
    body = await request.body()
    handler, model = await webhook_service.handle_webhook(payload, body, headers)

    background_tasks.add_task(handler, model, session)
