import datetime

from pydantic import BaseModel, ConfigDict, Field

from knowmydevs.core.utils import date_utils


class DiscussionQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_date: datetime.date | None = Field(
        None,
        alias="fromDate",
        title="From Date",
        description="Starting date to filter discussions",
        examples=[date_utils.days_ago(days=7)],
    )
    to_date: datetime.date | None = Field(
        None,
        alias="toDate",
        title="To Date",
        description="Filter discussions till the date",
        examples=[datetime.date.today()],
    )
    category_name: str | None = Field(
        None,
        alias="categoryName",
        title="Category Name",
        description="Filter discussions from the category name",
        examples=["Show and tell", "Questions", "Translations"],
    )
    limit: int = Field(
        10, le=100, title="Limit", description="Maximum items per page"
    )
    page: int = Field(1, ge=1, title="Offset", description="The page number")
