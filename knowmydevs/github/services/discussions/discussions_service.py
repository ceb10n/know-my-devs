from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, asc, delete, select

from knowmydevs.app_logger import logger
from knowmydevs.core.errors import BadRequestError, InternalError, NotFoundError
from knowmydevs.github.domain.discussion import Discussion
from knowmydevs.github.payloads.discussions import (
    CreateDiscussionPayload,
    UpdateDiscussionPayload,
)
from knowmydevs.github.responses.discussions import DiscussionResponse


def create_discussion(
    discussion: CreateDiscussionPayload, installation_id: int, session: Session
) -> DiscussionResponse:
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

    return DiscussionResponse(**discussion.model_dump())


def delete_discussion(
    discussion_id: int,
    installation_id: int,
    session: Session,
) -> None:
    logger.info(
        f"Deleting discussion {discussion_id} for installation {installation_id}"
    )
    statement = delete(Discussion).where(
        Discussion.id == discussion_id
        and Discussion.installation_id == installation_id
    )

    session.exec(statement)
    session.commit()


def find_discussion_by_id(
    discussion_id: int,
    installation_id: int,
    session: Session,
) -> DiscussionResponse:
    logger.info(
        f"Looking for discussion {discussion_id} for installation {installation_id}"
    )
    statement = select(Discussion).where(
        Discussion.id == discussion_id
        and Discussion.installation_id == installation_id
    )
    existing_discussion = session.exec(statement).one_or_none()

    if not existing_discussion:
        raise NotFoundError(f"Discussion with id {discussion_id} not found")

    return DiscussionResponse(**existing_discussion.model_dump())


def list_discussions(
    page: int,
    limit: int,
    installation_id: int,
    session: Session,
) -> list[DiscussionResponse]:
    logger.info(f"Listing discussions for installation {installation_id}")

    statement = (
        select(Discussion)
        .where(Discussion.installation_id == installation_id)
        .order_by(asc(Discussion.created_at))
        .limit(limit)
        .offset((page - 1) * limit)
    )

    discussions = session.exec(statement).all()

    return [DiscussionResponse(**d.model_dump()) for d in discussions]


def update_discussion(
    discussion_id: int,
    discussion: UpdateDiscussionPayload,
    installation_id: int,
    session: Session,
) -> DiscussionResponse:
    logger.info(
        f"Updating discussion {discussion_id} for installation {installation_id}"
    )

    statement = select(Discussion).where(
        Discussion.id == discussion_id
        and Discussion.installation_id == installation_id
    )
    existing_discussion = session.exec(statement).one_or_none()

    logger.debug(f"Discussion found: {existing_discussion.model_dump()}")

    if not existing_discussion:
        raise NotFoundError(f"Discussion with id {discussion_id} not found")

    for key, value in discussion.model_dump().items():
        try:
            logger.debug(f"Updating property {key} with value {value}")
            setattr(existing_discussion, key, value)

        except Exception as ex:
            err_msg = f"Invalid value {value} for property {key}"
            logger.debug(f"{err_msg}: {ex}")

            raise BadRequestError(err_msg) from ex

    logger.debug(
        f"Saving updated discussion: {existing_discussion.model_dump()}"
    )

    try:
        response = DiscussionResponse(**existing_discussion.model_dump())
        session.add(existing_discussion)
        session.commit()

        return response

    except Exception as ex:
        err_msg = f"Error updating discussion with id {discussion_id}"
        logger.error(f"{err_msg}: {ex}")
        session.rollback()

        raise InternalError(err_msg) from ex
