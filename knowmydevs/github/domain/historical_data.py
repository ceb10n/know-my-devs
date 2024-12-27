import datetime

from sqlmodel import BigInteger, Field, SQLModel


class HistoricalData(SQLModel, table=True):
    __tablename__ = "historical_data"

    installation_id: int = Field(
        ...,
        primary_key=True,
        sa_type=BigInteger,
        foreign_key="installations.id",
    )
    should_sync: bool = Field(..., default=True)
    has_prs_to_sync: bool = Field(..., default=True)
    has_discussions_to_sync: bool = Field(..., default=True)
    last_synced_at: datetime.datetime | None = Field(None)
