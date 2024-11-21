from enum import StrEnum, unique


@unique
class PullRequestStatus(StrEnum):
    OPEN = "open"
    CLOSED = "closed"