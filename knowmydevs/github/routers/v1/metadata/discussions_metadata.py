from knowmydevs.github.responses.discussions import DiscussionCreatedResponse, DiscussionUpdatedResponse

from .types import Metadata

create_discussion_metadata: Metadata = {
    "summary": "Create a new discussion",
    "description": "Create a new discussion for the installation",
    "operation_id": "create_discussion",
    "status_code": 201,
    "responses": {
        "201": {
            "description": "Discussion created successfully",
            "model": DiscussionCreatedResponse,
        }
    },
}

update_discussion_metadata: Metadata = {
    "summary": "Update discussion",
    "description": "Update an existing discussion for the installation",
    "operation_id": "update_discussion",
    "status_code": 200,
    "responses": {
        "201": {
            "description": "Discussion updated successfully",
            "model": DiscussionUpdatedResponse,
        }
    },
}
