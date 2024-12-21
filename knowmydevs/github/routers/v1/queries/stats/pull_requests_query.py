import datetime

from pydantic import BaseModel, ConfigDict, Field

from knowmydevs.core.utils import date_utils


class PullRequestsQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    merged_from_date: datetime.date | None = Field(
        None,
        alias="fromDate",
        title="From Date",
        description="Starting date to filter pull requests",
        examples=[date_utils.days_ago(days=7)],
    )
    merged_to_date: datetime.date | None = Field(
        None,
        alias="toDate",
        title="To Date",
        description="Filter pull requests till the date",
        examples=[datetime.date.today()],
    )
    repository_name: str | None = Field(
        None,
        alias="repositoryName",
        title="Repository Name",
        description="Filter pull requests from the repository",
        examples=["fastapi", "pydantic", "sqlmodel"],
    )
    limit: int = Field(
        10, le=100, title="Limit", description="Maximum items per page"
    )
    page: int = Field(1, ge=1, title="Offset", description="The page number")
