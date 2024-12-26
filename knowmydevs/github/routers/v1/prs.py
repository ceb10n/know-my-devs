from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from knowmydevs.core.auth.token import get_current_installation
from knowmydevs.core.infra.db import get_session
from knowmydevs.github.payloads.prs import (
    CreatePullRequestPayload,
    UpdatePullRequestPayload,
)
from knowmydevs.github.responses.prs import PullRequestResponse
from knowmydevs.github.routers.v1.metadata.prs_metadata import (
    create_pr_metadata,
    delete_pr_metadata,
    find_pr_by_id_metadata,
    list_prs_metadata,
    update_pr_metadata,
)
from knowmydevs.github.routers.v1.queries import PaginationQuery
from knowmydevs.github.services.pull_requests import pr_service

router = APIRouter(prefix="/pull-requests", tags=["Pull Requests"])


@router.get("/{pr_id}", **find_pr_by_id_metadata)
async def find_pr_by_id(
    pr_id: int,
    installation_id: int = Depends(get_current_installation),
    session: Session = Depends(get_session),
) -> PullRequestResponse:
    return pr_service.find_pull_request_by_id(
        pr_id, installation_id, session=session
    )


@router.get("", **list_prs_metadata)
async def list_pull_requests(
    pagination: Annotated[PaginationQuery, Query()],
    installation_id: int = Depends(get_current_installation),
    session: Session = Depends(get_session),
) -> list[PullRequestResponse]:
    return pr_service.list_pull_requests(
        **pagination.model_dump(),
        installation_id=installation_id,
        session=session,
    )


@router.post("", **create_pr_metadata)
async def create_pull_request(
    pull_request: CreatePullRequestPayload,
    installation_id: int = Depends(get_current_installation),
    session: Session = Depends(get_session),
) -> PullRequestResponse:
    return pr_service.create_pull_request(
        pull_request, installation_id, session=session
    )


@router.put("/{pr_id}", **update_pr_metadata)
async def update_pull_request(
    pr_id: int,
    pull_request: UpdatePullRequestPayload,
    installation_id: int = Depends(get_current_installation),
    session: Session = Depends(get_session),
) -> PullRequestResponse:
    return pr_service.update_pull_request(
        pr_id, pull_request, installation_id, session=session
    )


@router.delete("/{pr_id}", **delete_pr_metadata)
async def delete_pull_request(
    pr_id: int,
    installation_id: int = Depends(get_current_installation),
    session: Session = Depends(get_session),
) -> None:
    pr_service.delete_pull_request(pr_id, installation_id, session=session)
