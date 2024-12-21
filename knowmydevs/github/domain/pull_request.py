import datetime

from sqlmodel import BigInteger, Field, SQLModel, String

from .pull_request_state import PullRequestState


class PullRequest(SQLModel, table=True):
    __tablename__ = "pull_requests"

    id: int = Field(..., primary_key=True, sa_type=BigInteger)
    installation_id: int = Field(
        ..., sa_type=BigInteger, foreign_key="installations.id"
    )

    closed_at: datetime.datetime | None = Field(None)
    created_at: datetime.datetime
    merge_commit_sha: str | None = Field(None, max_length=200)
    merged: bool
    merged_at: datetime.datetime | None = Field(None)
    merged_by_id: int | None = Field(None, sa_type=BigInteger, index=True)
    merged_by_login: str | None = Field(None, max_length=150)
    merged_by_html_url: str | None = Field(None, max_length=1000)
    number: int = Field(..., sa_type=BigInteger)
    opened_by_id: int = Field(sa_type=BigInteger, index=True)
    opened_by_login: str = Field(..., max_length=150)
    repository_id: int = Field(..., sa_type=BigInteger, index=True)
    repository_name: str = Field(..., max_length=250, index=True)
    state: PullRequestState = Field(sa_type=String, max_length=10)
    title: str = Field(max_length=500)
    updated_at: datetime.datetime | None = Field(None)
    url: str = Field(max_length=500)
