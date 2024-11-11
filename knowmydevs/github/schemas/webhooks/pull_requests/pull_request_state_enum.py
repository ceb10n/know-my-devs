from enum import StrEnum, unique


@unique
class PullRequestStateEnum(StrEnum):

    OPEN = "open"
    CLOSED = "closed"