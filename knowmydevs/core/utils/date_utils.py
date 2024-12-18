import datetime

from knowmydevs.app_logger import logger


def maybe_str_to_datetime(value: str | None) -> datetime.datetime | None:
    if not value:
        return None

    if isinstance(value, datetime.datetime):
        logger.debug(f"Date {value} is already a datetime")
        return value

    return datetime.datetime.fromisoformat(value)


def days_ago(*, days: int) -> datetime.date:
    return datetime.date.today() - datetime.timedelta(days=days)
