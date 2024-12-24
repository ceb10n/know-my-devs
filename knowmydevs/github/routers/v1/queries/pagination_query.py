from pydantic import BaseModel, ConfigDict, Field


class PaginationQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    limit: int = Field(
        10, le=100, title="Limit", description="Maximum items per page"
    )
    page: int = Field(1, ge=1, title="Offset", description="The page number")
