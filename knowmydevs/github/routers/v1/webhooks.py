from typing import Annotated, Any

from fastapi import APIRouter, BackgroundTasks, Header

from knowmydevs.github.services.webhooks import webhook_service

router = APIRouter()


@router.post("/webhooks")
async def handle_webhook(
    payload: dict[str, Any],
    x_github_event: Annotated[str, Header()],
    background_tasks: BackgroundTasks,
):
    handler, model = webhook_service.handle_webhook(payload, x_github_event)

    background_tasks.add_task(handler, model, session)
