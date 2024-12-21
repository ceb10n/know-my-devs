from pydantic import BaseModel, ConfigDict, Field


class PullRequestStatsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    count: int = Field(
        ...,
        title="Count",
        description="The number of pull requests approved submitted the user",
    )

    user_id: int = Field(
        ...,
        alias="id",
        title="User Id",
        description="The id of the user who got the approved pull requests",
    )

    user_login: str = Field(
        ...,
        alias="login",
        title="User Login",
        description="The username of the user who got the approved pull requests",
    )

    user_url: str = Field(
        ...,
        alias="url",
        title="User URL",
        description="The url for the user's profile at github",
    )

    user_avatar_url: str | None = Field(
        None,
        alias="avatar",
        title="Avatar URL",
        description="The url for the user's avatar at github",
    )
