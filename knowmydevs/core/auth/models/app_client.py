from pydantic import BaseModel, Field


class AppClient(BaseModel):
    pool_id: str = Field(..., alias="UserPoolId")
    client_name: str = Field(..., alias="ClientName")
    client_id: str = Field(..., alias="ClientId")
    client_secret: str = Field(..., alias="ClientSecret")
