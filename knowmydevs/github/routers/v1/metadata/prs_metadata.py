from knowmydevs.github.responses.prs import PullRequestResponse

from .types import Metadata

create_pr_metadata: Metadata = {
    "summary": "Create a new pull request",
    "description": "Create a new pull_request for the installation",
    "operation_id": "create_pull_request",
    "status_code": 201,
    "responses": {
        "201": {
            "description": "Pull Request created successfully",
            "model": PullRequestResponse,
        }
    },
}


delete_pr_metadata: Metadata = {
    "summary": "Delete pull request",
    "description": "Delete an existing pull request by id for the installation",
    "operation_id": "delete_pull_request",
    "status_code": 204,
    "responses": {
        "204": {
            "description": "Pull Request successfully deleted or not found"
        },
    },
}


find_pr_by_id_metadata: Metadata = {
    "summary": "Find pull request",
    "description": "Find an existing pull request by id for the installation",
    "operation_id": "find_pr_by_id",
    "status_code": 200,
    "responses": {
        "200": {
            "description": "Pull Request found",
            "model": PullRequestResponse,
        },
        "404": {
            "description": "Pull Request not found",
        },
    },
}


list_prs_metadata: Metadata = {
    "summary": "List pull requests",
    "description": "List the pull requests for the installation",
    "operation_id": "list_pull_requests",
    "status_code": 200,
    "responses": {
        "200": {
            "description": "Pull Requests for the installation",
            "model": list[PullRequestResponse],
        }
    },
}


update_pr_metadata: Metadata = {
    "summary": "Update pull request",
    "description": "Update an existing pull request for the installation",
    "operation_id": "update_pull_request",
    "status_code": 200,
    "responses": {
        "200": {
            "description": "Pull Request updated successfully",
            "model": PullRequestResponse,
        },
        "404": {
            "description": "Pull Request not found",
        },
    },
}
