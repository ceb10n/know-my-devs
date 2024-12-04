from typing import Any

import logfire
from gh_hooks_utils.payloads import PullRequestEvent
from sqlmodel import Session, select

from knowmydevs.app_logger import logger
from knowmydevs.github.domain import PullRequest


async def handle(event: PullRequestEvent, session: Session) -> None:
    logger.info(f"Handling Pull Request Event for PR {event.pull_request.id}")
    with logfire.span("Github Pull Request Event"):
        pr_dict = adapt(event)

        pr = find_pull_request_by_id(
            id=event.pull_request.id,
            installation_id=event.installation.id,
            session=session,
        )

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


def find_pull_request_by_id(
    id: int, installation_id: int | None, session: Session
) -> PullRequest | None:
    with logfire.span("Find Pull Request by Id") as span:
        span.set_attribute("id", id)

        statement = select(PullRequest).where(PullRequest.id == id)
        if installation_id:
            statement = statement.where(
                PullRequest.installation_id == installation_id
            )

        results = session.exec(statement)

        return results.one_or_none()


def adapt(pr_event: PullRequestEvent) -> dict[str, Any]:
    optional_values: dict[str, Any] = {}

    if pr_event.installation:
        installation = pr_event.installation
        optional_values["installation_id"] = installation.id

    if pr_event.repository:
        repository = pr_event.repository
        optional_values["repository_id"] = repository.id
        optional_values["repository_name"] = repository.name

    if pr_event.pull_request.user:
        user = pr_event.pull_request.user
        optional_values["opened_by_id"] = user.id
        optional_values["opened_by_login"] = user.login

    if pr_event.pull_request.merged_by:
        user = pr_event.pull_request.merged_by
        optional_values["merged_by_id"] = user.id
        optional_values["merged_by_login"] = user.login

    return {
        **optional_values,
        "id": pr_event.pull_request.id,
        "number": pr_event.pull_request.number,
        "url": pr_event.pull_request.url,
        "state": pr_event.pull_request.state,
        "title": pr_event.pull_request.title,
        "merged": pr_event.pull_request.merged,
        "merge_commit_sha": pr_event.pull_request.merge_commit_sha,
        "created_at": pr_event.pull_request.created_at,
        "updated_at": pr_event.pull_request.updated_at,
        "closed_at": pr_event.pull_request.closed_at,
        "merged_at": pr_event.pull_request.merged_at,
    }
