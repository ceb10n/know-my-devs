from enum import StrEnum, unique


@unique
class PullRequestState(StrEnum):
    OPEN = "open"
    CLOSED = "closed"