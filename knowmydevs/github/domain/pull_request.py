import datetime

from sqlmodel import BigInteger, Field, SQLModel, String

from .pull_request_status import PullRequestStatus


class PullRequest(SQLModel, table=True):
    __tablename__ = "pull_requests"

    id: int = Field(primary_key=True, sa_type=BigInteger)
    url: str = Field(max_length=500)
    status: PullRequestStatus = Field(sa_type=String, max_length=10)
    title: str = Field(max_length=500)
    opened_by: int = Field(sa_type=BigInteger, foreign_key="users.id")
    merged_by: int = Field(sa_type=BigInteger, foreign_key="users.id")
    merged: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    closed_at: datetime.datetime
    merged_at: datetime.datetime