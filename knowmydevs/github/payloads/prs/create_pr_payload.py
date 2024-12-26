import datetime

from pydantic import BaseModel, ConfigDict, Field

from knowmydevs.github.domain.pull_request_state import PullRequestState


class CreatePullRequestPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(
        ...,
        alias="id",
        title="Id",
        description="Discussion id",
        examples=[123456],
    )
    closed_at: datetime.datetime | None = Field(
        None,
        alias="closedAt",
        title="Closed At",
        description="Date and time when the pull request was closed",
        examples=["2021-10-01T00:00:00Z"],
    )
    created_at: datetime.datetime = Field(
        ...,
        alias="createdAt",
        title="Created At",
        description="Date and time when the pull request was created",
        examples=["2021-10-01T00:00:00Z"],
    )
    merge_commit_sha: str | None = Field(
        None,
        alias="mergeCommitSha",
        max_length=200,
        title="Merge Commit Sha",
        description="Merge commit sha",
        examples=["a1b2c3d4e5f6g7h8i9j0"],
    )
    merged: bool = Field(
        False,
        alias="merged",
        title="Merged",
        description="Flag indicating if the pull request was merged",
        examples=[True, False],
    )
    merged_at: datetime.datetime | None = Field(
        None,
        alias="mergedAt",
        title="Merged At",
        description="Date and time when the pull request was merged",
        examples=["2021-10-01T00:00:00Z"],
    )
    merged_by_id: int | None = Field(
        None,
        alias="mergedById",
        title="Merged By User Id",
        description="Id from the user who merged the pull request",
        examples=[4321],
    )
    merged_by_login: str | None = Field(
        None,
        alias="mergedByLogin",
        max_length=150,
        title="Merged By User Login",
        description="Login from the user who merged the pull request",
        examples=["octocat", "ceb10n"],
    )
    merged_by_html_url: str | None = Field(
        None,
        alias="mergedByHtmlUrl",
        max_length=1000,
        title="Merged By User URL",
        description="URL from the user who merged the pull request",
        examples=["https://github.com/ceb10n", "https://github.com/octocat"],
    )
    number: int = Field(
        ...,
        alias="number",
        title="Number",
        description="Pull request number",
        examples=[1],
    )
    opened_by_id: int = Field(
        ...,
        alias="openedById",
        title="Opened By User Id",
        description="Id from the user who opened the pull request",
        examples=[4321],
    )
    opened_by_login: str = Field(
        ...,
        alias="openedByLogin",
        max_length=150,
        title="Opened By User Login",
        description="Login from the user who opened the pull request",
        examples=["octocat", "ceb10n"],
    )
    repository_id: int = Field(
        ...,
        alias="repositoryId",
        title="Repository Id",
        description="Id from the repository from the pull request",
        examples=[123456],
    )
    repository_name: str = Field(
        ...,
        alias="repositoryName",
        max_length=250,
        title="Repository Name",
        description="Name from the repository from the pull request",
        examples=["octocat/hello-world"],
    )
    state: PullRequestState = Field(
        ...,
        alias="state",
        title="State",
        description="Pull request state",
        examples=["open", "closed"],
    )
    title: str = Field(
        ...,
        alias="title",
        max_length=500,
        title="Title",
        description="Pull request title",
        examples=["Add new feature", "Fix bug"],
    )
    updated_at: datetime.datetime | None = Field(
        None,
        alias="updatedAt",
        title="Updated At",
        description="Date and time when the pull request was updated",
        examples=["2021-10-01T00:00:00Z"],
    )
    url: str = Field(
        ...,
        max_length=500,
        title="URL",
        description="Pull request URL",
        examples=["https://github.com/octocat/Spoon-Knife/issues/1"]
    )
