from pydantic import BaseModel, Field


class TokenForm(BaseModel):
    grant_type: str = Field(
        ...,
        pattern="client_credentials",
        title="Grant Type",
        description="Grant type to authorize access",
        examples=["client_credentials"],
    )
