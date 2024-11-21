from gh_hooks_utils.payloads import PullRequestEvent
from sqlmodel import Session

from knowmydevs.app_logger import logger
from knowmydevs.github.domain import PullRequest


async def handle(event: PullRequestEvent, session: Session) -> None:
    logger.debug("Handling pull request event")

    pull_request = PullRequest(
        id=event.pull_request.id,
        url=event.pull_request.url,
        state=event.pull_request.state,
        title=event.pull_request.title,
        opened_by=event.pull_request.user.id,
        merged=event.pull_request.merged,
        created_at=event.pull_request.created_at,
        updated_at=event.pull_request.updated_at
    )

    if event.is_merged():
        pull_request.merged_by = event.pull_request.merged_by.id
        pull_request.merged_at = event.pull_request.merged_at

    if event.is_closed():
        pull_request.closed_at = event.pull_request.closed_at

    session.add(pull_request)
    session.commit()