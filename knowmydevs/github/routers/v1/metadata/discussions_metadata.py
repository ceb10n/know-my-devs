from knowmydevs.github.responses.discussions import DiscussionResponse

from .types import Metadata

create_discussion_metadata: Metadata = {
    "summary": "Create a new discussion",
    "description": "Create a new discussion for the installation",
    "operation_id": "create_discussion",
    "status_code": 201,
    "responses": {
        "201": {
            "description": "Discussion created successfully",
            "model": DiscussionResponse,
        }
    },
}


delete_discussion_metadata: Metadata = {
    "summary": "Delete discussion",
    "description": "Delete an existing discussion by id for the installation",
    "operation_id": "delete_discussion",
    "status_code": 204,
    "responses": {
        "204": {"description": "Discussion successfully deleted or not found"},
    },
}


find_discussion_by_id_metadata: Metadata = {
    "summary": "Find discussion",
    "description": "Find an existing discussion by id for the installation",
    "operation_id": "find_discussion_by_id",
    "status_code": 200,
    "responses": {
        "200": {
            "description": "Discussion found",
            "model": DiscussionResponse,
        },
        "404": {
            "description": "Discussion not found",
        },
    },
}


list_discussions_metadata: Metadata = {
    "summary": "List discussions",
    "description": "List the discussions for the installation",
    "operation_id": "list_discussions",
    "status_code": 200,
    "responses": {
        "200": {
            "description": "Discussions for the installation",
            "model": list[DiscussionResponse],
        }
    },
}


update_discussion_metadata: Metadata = {
    "summary": "Update discussion",
    "description": "Update an existing discussion for the installation",
    "operation_id": "update_discussion",
    "status_code": 200,
    "responses": {
        "200": {
            "description": "Discussion updated successfully",
            "model": DiscussionResponse,
        },
        "404": {
            "description": "Discussion not found",
        },
    },
}
