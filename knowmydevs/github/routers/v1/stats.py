from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from knowmydevs.core.auth.token import get_current_installation
from knowmydevs.core.infra.db import get_session
from knowmydevs.github.responses.stats import (
    DiscussionStatsResponse,
    PullRequestStatsResponse,
)
from knowmydevs.github.routers.v1.metadata.stats_metadata import (
    discussion_metadata,
    pull_request_metadata,
)
from knowmydevs.github.routers.v1.queries.stats import (
    DiscussionQuery,
    PullRequestsQuery,
)
from knowmydevs.github.services.stats import discussion_service, pr_service

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/discussions", **discussion_metadata)
async def list_discussion_stats(
    query: Annotated[DiscussionQuery, Query()],
    installation_id: int = Depends(get_current_installation),
    session: Session = Depends(get_session),
) -> list[DiscussionStatsResponse]:
    return discussion_service.overall_stats(
        installation_id, session=session, **query.model_dump()
    )


@router.get("/pull-requests", **pull_request_metadata)
async def list_pr_stats(
    query: Annotated[PullRequestsQuery, Query()],
    installation_id: int = Depends(get_current_installation),
    session: Session = Depends(get_session),
) -> list[PullRequestStatsResponse]:
    return pr_service.overall_stats(
        installation_id, session=session, **query.model_dump()
    )
