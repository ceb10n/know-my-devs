from knowmydevs.github.responses.stats import (
    DiscussionStatsResponse,
    PullRequestStatsResponse,
)

from .types import Metadata

discussion_metadata: Metadata = {
    "summary": "List stats from discussions",
    "description": "List the users who have most accepted answers in discussions",
    "operation_id": "list_discussion_stats",
    "responses": {
        "200": {
            "description": "List of discussions stats",
            "model": list[DiscussionStatsResponse],
        }
    },
}


pull_request_metadata: Metadata = {
    "summary": "List stats from pull requests",
    "description": "List the users who have most approved pull requests",
    "operation_id": "list_pull_request_stats",
    "responses": {
        "200": {
            "description": "List of users who have most pull requests approved",
            "model": list[PullRequestStatsResponse],
        }
    },
}
