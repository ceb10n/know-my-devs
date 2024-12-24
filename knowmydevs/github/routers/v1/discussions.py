from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from knowmydevs.core.auth.token import get_current_installation
from knowmydevs.core.infra.db import get_session
from knowmydevs.github.payloads.discussions import (
    CreateDiscussionPayload,
    UpdateDiscussionPayload,
)
from knowmydevs.github.responses.discussions import DiscussionResponse
from knowmydevs.github.routers.v1.metadata.discussions_metadata import (
    create_discussion_metadata,
    delete_discussion_metadata,
    find_discussion_by_id_metadata,
    list_discussions_metadata,
    update_discussion_metadata,
)
from knowmydevs.github.routers.v1.queries import PaginationQuery
from knowmydevs.github.services.discussions import discussions_service

router = APIRouter(prefix="/discussions", tags=["Discussions"])


@router.get("/{discussion_id}", **find_discussion_by_id_metadata)
async def find_discussion_by_id(
    discussion_id: int,
    installation_id: int = Depends(get_current_installation),
    session: Session = Depends(get_session),
) -> DiscussionResponse:
    return discussions_service.find_discussion_by_id(
        discussion_id, installation_id, session=session
    )


@router.get("", **list_discussions_metadata)
async def list_discussions(
    pagination: Annotated[PaginationQuery, Query()],
    installation_id: int = Depends(get_current_installation),
    session: Session = Depends(get_session),
) -> list[DiscussionResponse]:
    return discussions_service.list_discussions(
        **pagination.model_dump(),
        installation_id=installation_id,
        session=session,
    )


@router.post("", **create_discussion_metadata)
async def create_discussion(
    discussion: CreateDiscussionPayload,
    installation_id: int = Depends(get_current_installation),
    session: Session = Depends(get_session),
) -> DiscussionResponse:
    return discussions_service.create_discussion(
        discussion, installation_id, session=session
    )


@router.put("/{discussion_id}", **update_discussion_metadata)
async def update_discussion(
    discussion_id: int,
    discussion: UpdateDiscussionPayload,
    installation_id: int = Depends(get_current_installation),
    session: Session = Depends(get_session),
) -> DiscussionResponse:
    return discussions_service.update_discussion(
        discussion_id, discussion, installation_id, session=session
    )


@router.delete("/{discussion_id}", **delete_discussion_metadata)
async def delete_discussion(
    discussion_id: int,
    installation_id: int = Depends(get_current_installation),
    session: Session = Depends(get_session),
) -> None:
    discussions_service.delete_discussion(
        discussion_id, installation_id, session=session
    )
