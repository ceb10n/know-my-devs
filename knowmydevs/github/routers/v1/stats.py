from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from knowmydevs.core.auth.token import get_current_installation
from knowmydevs.core.infra.db import get_session
from knowmydevs.github.routers.v1.queries.stats import DiscussionQuery
from knowmydevs.github.services.stats import discussion_service

router = APIRouter(tags=["Stats"])


@router.get("/discussions", status_code=200)
async def handle_webhook(
    query: Annotated[DiscussionQuery, Query()],
    installation_id: int = Depends(get_current_installation),
    session: Session = Depends(get_session),
):
    return discussion_service.overall_stats(
        installation_id, session=session, **query.model_dump()
    )
