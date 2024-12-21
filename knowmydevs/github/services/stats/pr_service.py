import datetime
from typing import Any

from pydantic import ValidationError
from sqlmodel import Date, Session, cast, desc, func, select
from sqlmodel.sql.expression import Select

from knowmydevs.app_logger import logger
from knowmydevs.core.errors import InternalError, UnauthorizedError
from knowmydevs.github.domain import PullRequest
from knowmydevs.github.responses import PullRequestStatsResponse


def overall_stats(
    installation_id: int,
    *,
    merged_from_date: datetime.date | None,
    merged_to_date: datetime.date | None,
    repository_name: str | None,
    limit: int,
    page: int,
    session: Session,
) -> list[PullRequestStatsResponse]:
    logger.info(f"Listing pull requests for installation {installation_id}")

    if not installation_id:
        raise UnauthorizedError("Installation id is required")

    statement = select(
        func.count(PullRequest.id).label("total"),
        PullRequest.merged_by_login,
        PullRequest.merged_by_id,
        PullRequest.merged_by_html_url,
    ).where(
        PullRequest.installation_id == installation_id
        and PullRequest.merged_by_id is not None
        and PullRequest.merged_by_login is not None
        and PullRequest.merged_by_html_url is not None
    )

    statement = _add_filters_to_query(
        statement, merged_from_date, merged_to_date, repository_name
    )

    statement = (
        statement.group_by(
            PullRequest.merged_by_login,
            PullRequest.merged_by_id,
            PullRequest.merged_by_html_url,
        )
        .order_by(desc("total"))
        .limit(limit)
        .offset((page - 1) * limit)
    )

    response = session.exec(statement).fetchall()

    return adapt(response)


def adapt(response: list[tuple[Any, ...]]) -> list[PullRequestStatsResponse]:
    try:
        return [
            PullRequestStatsResponse(
                count=row[0],
                user_login=row[1],
                user_id=row[2],
                user_url=row[3],
                user_avatar_url=f"{row[3]}.png",
            )
            for row in response
        ]
    except ValidationError as val_err:
        raise InternalError(
            "An error occurred while fetching pull requests"
        ) from val_err


def _add_filters_to_query(
    statement: Select,
    merged_from_date: datetime.date | None,
    merged_to_date: datetime.date | None,
    repository_name: str | None,
) -> Select:
    try:
        if merged_from_date:
            logger.debug(f"Filter merged_from_date: {merged_from_date}")
            statement = statement.where(
                cast(PullRequest.merged_at, Date) >= merged_from_date
            )

        if merged_to_date:
            logger.debug(f"Filter merged_to_date: {merged_to_date}")
            statement = statement.where(
                cast(PullRequest.merged_at, Date) <= merged_to_date
            )

        if repository_name:
            statement = statement.where(
                PullRequest.repository_name == repository_name
            )
        return statement
    except Exception as ex:
        raise InternalError(
            "An error occurred while fetching pull requests"
        ) from ex
