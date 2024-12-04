from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header, Request
from gh_hooks_utils.headers import WebhookHeaders
from sqlmodel import Session

from knowmydevs.core.infra.db import get_session
from knowmydevs.github.services.webhooks import webhook_service

router = APIRouter()


@router.post("/webhooks", status_code=204)
async def handle_webhook(
    request: Request,
    payload: dict[str, Any],
    headers: Annotated[WebhookHeaders, Header()],
    session: Session = Depends(get_session),
) -> None:
    body = await request.body()
    await webhook_service.handle_webhook(payload, body, headers, session)
