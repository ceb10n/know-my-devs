from pydantic import BaseModel, ConfigDict, Field


class DiscussionStatsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    count: int = Field(
        ...,
        title="Count",
        description="The number of answered questions by the user",
    )
    user_id: int = Field(
        ...,
        alias="userId",
        title="User Id",
        description="The user id of the user who answered the questions",
    )
    user_login: str = Field(
        ...,
        alias="login",
        title="User Login",
        description="The username of the user who answered the questions",
    )
    user_avatar_url: str | None = Field(
        None,
        alias="avatar",
        title="Avatar URL",
        description="The url for the user's avatar at github",
    )
    user_html_url: str = Field(
        ...,
        alias="url",
        title="User URL",
        description="The url for the user's profile at github",
    )
    category_name: str = Field(
        ...,
        alias="category",
        title="Category Name",
        description="The name of the category that the user answered the questions",
    )
