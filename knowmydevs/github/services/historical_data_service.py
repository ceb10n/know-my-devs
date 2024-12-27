from sqlmodel import Session, select

from knowmydevs.github.domain import HistoricalData


def list_all_that_need_to_sync(
    page: int, limit: int, session: Session
) -> list[HistoricalData]:
    statement = (
        select(HistoricalData)
        .where(HistoricalData.should_sync is True)
        .limit(limit)
        .offset((page - 1) * limit)
    )

    return session.exec(statement).all()
