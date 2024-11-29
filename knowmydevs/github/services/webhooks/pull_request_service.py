from typing import Any

import logfire
from gh_hooks_utils.payloads import PullRequestEvent
from sqlmodel import Session, select

from knowmydevs.app_logger import logger
from knowmydevs.github.domain import PullRequest


async def handle(event: PullRequestEvent, session: Session) -> None:
    with logfire.span("Github Pull Request Event"):
        pr_dict = adapt(event)

        pr = find_pull_request_by_id(event.pull_request.id, session)

        if pr:
            logger.debug(f"Updating Pull Request {event.pull_request.id}")
            for k, v in pr_dict.items():
                setattr(pr, k, v)

        else:
            logger.debug(f"Creating Pull Request {event.pull_request.id}")
            pr = PullRequest(**pr_dict)

        session.add(pr)
        session.commit()

        logger.info("Pull Request Event successfully handled")


def find_pull_request_by_id(id: int, session: Session) -> PullRequest | None:
    with logfire.span("Find Pull Request by Id") as span:
        span.set_attribute("id", id)

        statement = select(PullRequest).where(PullRequest.id == id)
        results = session.exec(statement)

        return results.one_or_none()


def adapt(pr_event: PullRequestEvent) -> dict[str, Any]:
    merged_by_dict = {}

    if pr_event.pull_request.merged_by:
        merged_by_dict["merged_by"] = pr_event.pull_request.merged_by.id

    return {
        **merged_by_dict,
        "id": pr_event.pull_request.id,
        "url": pr_event.pull_request.url,
        "state": pr_event.pull_request.state,
        "title": pr_event.pull_request.title,
        "opened_by": pr_event.pull_request.user.id,
        "merged": pr_event.pull_request.merged,
        "created_at": pr_event.pull_request.created_at,
        "updated_at": pr_event.pull_request.updated_at,
        "closed_at": pr_event.pull_request.closed_at,
        "merged_at": pr_event.pull_request.merged_at,
    }
