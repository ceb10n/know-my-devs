import datetime

from sqlmodel import BigInteger, Field, SQLModel


class Discussion(SQLModel, table=True):
    __tablename__ = "discussions"

    id: int = Field(..., primary_key=True, sa_type=BigInteger)
    installation_id: int = Field(
        ..., sa_type=BigInteger, foreign_key="installations.id"
    )
    number: int = Field(..., sa_type=BigInteger)
    answer_by_id: int | None = Field(None, sa_type=BigInteger, index=True)
    answer_by_login: str | None = Field(None, max_length=150, index=True)
    answer_chosen_by_id: int | None = Field(None, sa_type=BigInteger)
    answer_chosen_by_login: str | None = Field(None, max_length=150)
    answer_chosen_at: datetime.datetime | None = Field(None, index=True)
    category_id: int = Field(..., sa_type=BigInteger, index=True)
    category_name: str = Field(..., max_length=100)
    created_at: datetime.datetime
    state: str = Field(..., max_length=30)
    state_reason: str = Field(..., max_length=30)
    title: str = Field(..., max_length=500)
    updated_at: datetime.datetime | None = Field(None)
    opened_by_id: int = Field(sa_type=BigInteger, index=True)
    opened_by_login: str = Field(..., max_length=150)
    repository_id: int = Field(..., sa_type=BigInteger, index=True)
    repository_name: str = Field(..., max_length=250, index=True)
