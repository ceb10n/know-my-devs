from typing import Any

import logfire
from gh_hooks_utils.payloads import DiscussionEvent
from sqlmodel import Session, select

from knowmydevs.app_logger import logger
from knowmydevs.core.utils import date_utils
from knowmydevs.github.domain import Discussion


async def handle(event: DiscussionEvent, session: Session) -> None:
    with logfire.span("Discussion Event"):
        logger.info("Handling Discussion Event")
        discussion_dict = adapt(event)

        discussion = find_discussion_by_id(
            id=event.discussion.id, session=session
        )

        if discussion:
            logger.debug(f"Updating Discussion {event.discussion.id}")
            for k, v in discussion_dict.items():
                setattr(discussion, k, v)

        else:
            logger.debug(f"Creating Discussion {event.discussion.id}")
            discussion = Discussion(**discussion_dict)

        session.add(discussion)
        session.commit()

        logger.info(
            f"Discussion Event with id {discussion.id} successfully handled"
        )


def find_discussion_by_id(id: int, session: Session) -> Discussion | None:
    with logfire.span("Find Discussion By Id") as span:
        span.set_attribute("id", id)

        statement = select(Discussion).where(Discussion.id == id)
        results = session.exec(statement)

        return results.one_or_none()


def adapt(discussion_event: DiscussionEvent) -> dict[str, Any]:
    optional_values: dict[str, Any] = {}

    if not discussion_event.discussion:
        raise ValueError("Field discussion is required")

    if not discussion_event.installation:
        raise ValueError("Field installation is required")

    if discussion_event.answer:
        answer = discussion_event.answer
        optional_values["answer_by_id"] = answer.user.id
        optional_values["answer_by_login"] = answer.user.login

    if discussion_event.discussion.answer_chosen_by:
        user = discussion_event.discussion.answer_chosen_by
        optional_values["answer_chosen_by_id"] = user.id
        optional_values["answer_chosen_by_login"] = user.login

    if discussion_event.repository:
        repository = discussion_event.repository
        optional_values["repository_id"] = repository.id
        optional_values["repository_name"] = repository.name

    if discussion_event.discussion.state_reason:
        optional_values["state_reason"] = discussion_event.discussion.state_reason.value,

    return {
        **optional_values,
        "id": discussion_event.discussion.id,
        "installation_id": discussion_event.installation.id,
        "category_id": discussion_event.discussion.category.id,
        "category_name": discussion_event.discussion.category.name,
        "number": discussion_event.discussion.number,
        "state": discussion_event.discussion.state.value,
        "title": discussion_event.discussion.title,
        "opened_by_id": discussion_event.discussion.user.id,
        "opened_by_login": discussion_event.discussion.user.login,
        "created_at": date_utils.maybe_str_to_datetime(
            discussion_event.discussion.created_at
        ),
        "updated_at": date_utils.maybe_str_to_datetime(
            discussion_event.discussion.updated_at
        ),
        "answer_chosen_at": date_utils.maybe_str_to_datetime(
            discussion_event.discussion.answer_chosen_at
        ),
    }
