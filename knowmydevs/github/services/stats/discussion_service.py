import datetime
from typing import Any

from pydantic import ValidationError
from sqlalchemy import desc, select, Select
from sqlmodel import Session, func

from knowmydevs.app_logger import logger
from knowmydevs.core.errors import InternalError, UnauthorizedError
from knowmydevs.github.domain import Discussion
from knowmydevs.github.responses import DiscussionStatsResponse


def overall_stats(
    installation_id: int,
    *,
    from_date: datetime.date | None,
    to_date: datetime.date | None,
    category_name: str | None,
    limit: int,
    page: int,
    session: Session,
) -> list[DiscussionStatsResponse]:
    logger.info(f"Listing discussions for installation {installation_id}")

    if not installation_id:
        raise UnauthorizedError("Installation id is required")

    statement = select(
        func.count(Discussion.id).label("total"),
        Discussion.answer_by_login,
        Discussion.answer_by_id,
        Discussion.answer_chosen_by_html_url,
        Discussion.category_name,
    ).where(
        Discussion.installation_id == installation_id
        and Discussion.answer_by_id is not None
    )

    statement = _add_filters_to_query(
        statement, from_date, to_date, category_name
    )

    if from_date:
        statement = statement.where(Discussion.answer_chosen_at >= from_date)

    if to_date:
        statement = statement.where(Discussion.answer_chosen_at <= to_date)

    if category_name:
        statement = statement.where(Discussion.category_name == category_name)

    statement = (
        statement.group_by(
            Discussion.answer_by_login,
            Discussion.answer_by_id,
            Discussion.answer_chosen_by_html_url,
            Discussion.category_name,
        )
        .order_by(desc("total"))
        .limit(limit)
        .offset((page - 1) * limit)
    )

    response = session.exec(statement).fetchall()

    return adapt(response)


def adapt(response: list[tuple[Any]]) -> list[DiscussionStatsResponse]:
    try:
        return [
            DiscussionStatsResponse(
                count=item[0],
                user_login=item[1],
                user_id=item[2],
                user_avatar_url=f"{item[3]}.png",
                user_html_url=item[3],
                category_name=item[4],
            )
            for item in response
        ]
    except ValidationError as val_ex:
        logger.warning(
            f"Error mapping database results to DiscussionStatsResponse: {val_ex}"
        )
        _raise_internal(val_ex)


def _add_filters_to_query(
    statement: Select,
    from_date: datetime.date | None,
    to_date: datetime.date | None,
    category_name: str | None,
) -> Select:
    try:
        if from_date:
            statement = statement.where(
                Discussion.answer_chosen_at >= from_date
            )

        if to_date:
            statement = statement.where(Discussion.answer_chosen_at <= to_date)

        if category_name:
            statement = statement.where(
                Discussion.category_name == category_name
            )

        return statement
    except Exception as ex:
        _raise_internal(ex)


def _raise_internal(ex: type[Exception]) -> None:
    raise InternalError("An error occurred while fetching discussions") from ex
