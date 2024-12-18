import datetime

from sqlmodel import BigInteger, Field, SQLModel


class AppClient(SQLModel, table=True):
    __tablename__ = "app_clients"

    id: int = Field(
        ...,
        primary_key=True,
        sa_type=BigInteger,
        foreign_key="installations.id",
    )
    user_pool_id: str = Field(..., max_length=50)
    client_id: str = Field(..., max_length=50)
    client_name: str = Field(..., max_length=50)
    partial_secret: str = Field(..., max_length=5)
    created_at: datetime.datetime
