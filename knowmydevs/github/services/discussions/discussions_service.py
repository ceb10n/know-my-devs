from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from knowmydevs.app_logger import logger
from knowmydevs.core.errors import BadRequestError, InternalError, NotFoundError
from knowmydevs.github.domain.discussion import Discussion
from knowmydevs.github.payloads.discussions import (
    CreateDiscussionPayload,
    UpdateDiscussionPayload,
)
from knowmydevs.github.responses.discussions import DiscussionCreatedResponse


def create_discussion(
    discussion: CreateDiscussionPayload, installation_id: int, session: Session
) -> DiscussionCreatedResponse:
    logger.info(
        f"Creating discussion {discussion.id} for installation {installation_id}"
    )
    new_discussion = Discussion(
        installation_id=installation_id, **discussion.model_dump()
    )

    try:
        session.add(new_discussion)
        session.commit()

    except IntegrityError as ex:
        logger.warning(f"Discussion alreay exists: {ex}")
        session.rollback()

        raise BadRequestError("Discussion already exists") from ex

    except Exception as ex:
        logger.error(f"Error creating discussion: {ex}")
        session.rollback()

        raise InternalError("Error creating discussion") from ex

    return DiscussionCreatedResponse(**discussion.model_dump())


def update_discussion(
    discussion_id: int,
    discussion: UpdateDiscussionPayload,
    installation_id: int,
    session: Session,
) -> DiscussionCreatedResponse:
    logger.info(
        f"Updating discussion {discussion_id} for installation {installation_id}"
    )

    statement = select(Discussion).where(Discussion.id == discussion_id)
    existing_discussion = session.exec(statement).one_or_none()

    if not existing_discussion:
        raise NotFoundError(f"Discussion with id {discussion_id} not found")

    for key, value in discussion.model_dump().items():
        try:
            setattr(existing_discussion, key, value)

        except Exception as ex:
            err_msg = f"Invalid value {value} for property {key}"
            logger.debug(f"{err_msg}: {ex}")

            raise BadRequestError(err_msg) from ex

    try:
        session.add(existing_discussion)
        session.commit()

    except Exception as ex:
        err_msg = f"Error updating discussion with id {discussion_id}"
        logger.error(f"{err_msg}: {ex}")
        session.rollback()

        raise InternalError(err_msg) from ex

    return DiscussionCreatedResponse(**discussion.model_dump())
