from pydantic import BaseModel

from knowmydevs.github.schemas.webhooks import (
    Enterprise,
    Installation,
    Organization,
    Repository,
    User,
)

from .pull_request import PullRequest
from .pull_request_action_enum import PullRequestActionEnum


class PullRequestEvent(BaseModel):
    action: PullRequestActionEnum
    enterprise: Enterprise | None = None
    installation: Installation | None = None
    number: int
    organization: Organization | None = None
    pull_request: PullRequest
    repository: Repository
    sender: User
