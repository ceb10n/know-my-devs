from pydantic import BaseModel, Field


class TokenCredential(BaseModel):
    username: str = Field(
        ...,
        title="Username",
        description="App Client Id",
        examples=["1abcd2abcde12abcdef12abcd1"],
    )
    password: str = Field(
        ...,
        title="Password",
        description="App Client Secret",
        examples=["abc12d3ef4g5hijkrsabcd12a3bacbd1abcde1abc1a12ab1ab"],
    )
