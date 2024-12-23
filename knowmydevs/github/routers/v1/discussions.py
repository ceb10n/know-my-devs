from fastapi import APIRouter, Depends
from sqlmodel import Session

from knowmydevs.core.auth.token import get_current_installation
from knowmydevs.core.infra.db import get_session
from knowmydevs.github.payloads.discussions import (
    CreateDiscussionPayload,
    UpdateDiscussionPayload,
)
from knowmydevs.github.responses.discussions import DiscussionCreatedResponse
from knowmydevs.github.routers.v1.metadata.discussions_metadata import (
    create_discussion_metadata,
    update_discussion_metadata,
)
from knowmydevs.github.services.discussions import discussions_service

router = APIRouter(prefix="/discussions", tags=["Discussions"])


@router.post("", **create_discussion_metadata)
async def create_discussion(
    discussion: CreateDiscussionPayload,
    installation_id: int = Depends(get_current_installation),
    session: Session = Depends(get_session),
) -> DiscussionCreatedResponse:
    return discussions_service.create_discussion(
        discussion, installation_id, session=session
    )


@router.put("/{discussion_id}", **update_discussion_metadata)
async def update_discussion(
    discussion_id: int,
    discussion: UpdateDiscussionPayload,
    installation_id: int = Depends(get_current_installation),
    session: Session = Depends(get_session),
) -> DiscussionCreatedResponse:
    return discussions_service.update_discussion(
        discussion_id, discussion, installation_id, session=session
    )
