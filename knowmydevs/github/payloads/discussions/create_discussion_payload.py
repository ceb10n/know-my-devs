import datetime

from gh_hooks_utils.payloads.discussions import (
    DiscussionStateEnum,
    DiscussionStateReasonEnum,
)
from pydantic import BaseModel, ConfigDict, Field


class CreateDiscussionPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(
        ...,
        alias="id",
        title="Id",
        description="Discussion id",
        examples=[123456],
    )
    number: int = Field(
        ...,
        alias="number",
        title="Number",
        description="Discussion number",
        examples=[1],
    )
    answer_by_id: int | None = Field(
        None,
        alias="answerByUserId",
        title="User Id from Answer",
        description="Id from the user who answered the discussion",
        examples=[4321],
    )
    answer_by_login: str | None = Field(
        None,
        alias="answerByUserLogin",
        max_length=150,
        title="Login from Answer",
        description="Login from the user who answered the discussion",
        examples=["octocat", "ceb10n"],
    )
    answer_chosen_by_id: int | None = Field(
        None,
        alias="answerChosenByUserId",
        title="User Id from who chose the Answer",
        description="Id from the user who chose the answer",
        examples=[4321],
    )
    answer_chosen_by_login: str | None = Field(
        None,
        alias="answerChosenByUserLogin",
        max_length=150,
        title="User Login from who chose the Answer",
        description="Login from the user who chose the answer",
        examples=["octocat", "ceb10n"],
    )
    answer_chosen_by_avatar_url: str | None = Field(
        None,
        alias="answerChosenByUserAvatar",
        max_length=1000,
        title="User Avatar from who chose the Answer",
        description="Avatar from the user who chose the answer",
        examples=["https://avatars.githubusercontent.com/u/235213?v=4"],
    )
    answer_chosen_by_html_url: str | None = Field(
        None,
        alias="answerChosenByUserUrl",
        max_length=1000,
        title="User URL from who chose the Answer",
        description="URL from the user who chose the answer",
        examples=["https://github.com/ceb10n", "https://github.com/octocat"],
    )
    answer_chosen_at: datetime.datetime | None = Field(
        None,
        alias="answerChosenAt",
        title="Answer Chosen At",
        description="Date when the answer was chosen",
        examples=["2021-10-01T00:00:00Z"],
    )
    category_id: int = Field(
        ...,
        alias="categoryId",
        title="Category Id",
        description="Category id",
        examples=[987654],
    )
    category_name: str = Field(
        ...,
        alias="categoryName",
        max_length=100,
        title="Category Name",
        description="The name of the category",
        examples=["Show & Tell", "Q&A"],
    )
    created_at: datetime.datetime = Field(
        ...,
        alias="createdAt",
        title="Created At",
        description="Date when the discussion was created",
        examples=["2021-10-01T00:00:00Z"],
    )
    state: str = Field(
        ...,
        alias="state",
        max_length=30,
        title="State",
        description="Discussion state",
        examples=[
            DiscussionStateEnum.LOCKED.value,
            DiscussionStateEnum.CLOSED.value,
        ],
    )
    state_reason: str | None = Field(
        None,
        alias="stateReason",
        max_length=30,
        title="State Reason",
        description="Reason for the discussion state",
        examples=[
            DiscussionStateReasonEnum.OUTDATED.value,
            DiscussionStateReasonEnum.RESOLVED.value,
            DiscussionStateReasonEnum.DUPLICATE.value,
        ],
    )
    title: str = Field(
        ...,
        alias="title",
        max_length=500,
        title="Title",
        description="Discussion's title",
        examples=[
            "[Github Actions] FastAPI People keep failing due to rate limiting",
            "FastAPI Docs & Translations Management",
        ],
    )
    updated_at: datetime.datetime | None = Field(
        None,
        alias="updatedAt",
        title="Updated At",
        description="Date when the discussion was updated",
        examples=["2021-10-01T00:00:00Z"],
    )
    opened_by_id: int = Field(
        ...,
        alias="openedByUserId",
        title="Opened By User Id",
        description="Id from the user who opened the discussion",
        examples=[235213],
    )
    opened_by_login: str = Field(
        ...,
        alias="openByUserLogin",
        max_length=150,
        title="Opened By User Login",
        description="Login from the user who opened the discussion",
        examples=["tiangolo", "ceb10n"],
    )
    repository_id: int = Field(
        ...,
        alias="repositoryId",
        title="Repository Id",
        description="Id from the repository the discussion started",
        examples=[160919119],
    )
    repository_name: str = Field(
        ...,
        alias="repositoryName",
        max_length=250,
        title="Repository Name",
        description="Name from the repository the discussion started",
        examples=["fastapi", "sqlmodel", "pydantic"],
    )
