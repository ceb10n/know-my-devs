import datetime

from sqlmodel import BigInteger, Field, SQLModel


class Installation(SQLModel, table=True):
    __tablename__ = "installations"

    id: int = Field(primary_key=True, sa_type=BigInteger)
    enterprise_id: int | None = Field(None, sa_type=BigInteger)
    enterprise_name: str | None = Field(None, max_length=150)
    organization_id: int | None = Field(None, sa_type=BigInteger)
    organization_login: str | None = Field(None, max_length=150)
    sender_id: int = Field(..., sa_type=BigInteger)
    sender_name: str | None = Field(None, max_length=150)
    sender_login: str = Field(..., max_length=150)
    installed_at: datetime.datetime
    updated_at: datetime.datetime | None = Field(None)
