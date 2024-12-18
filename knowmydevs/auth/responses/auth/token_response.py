from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str = Field(
        ...,
        title="Access Token",
        description="Issued access token",
        examples=["eyJraWQiOiJ.yJzdWIiOiIxZmd0cjFwcWdycDg.XARjdUcs6M8w4O"],
    )
    expires_in: int = Field(
        ...,
        title="Expires in",
        description="Duration of the access token in seconds",
        examples=[3600],
    )
    token_type: str = Field(
        "Bearer",
        title="Token Type",
        description="The type of the token. It's always Bearer",
    )
