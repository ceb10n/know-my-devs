import logfire
from gh_hooks_utils.payloads import PullRequestEvent
from sqlmodel import Session

from knowmydevs.github.domain import PullRequest
from knowmydevs.github.services import user_service


async def handle(event: PullRequestEvent, session: Session) -> None:
    logfire.debug("Handling pull request event")
    with logfire.span("Handling pull request {pr}", pr=event.pull_request.id):
        created_by = user_service.find_by_id(event.pull_request.user.id, session)

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