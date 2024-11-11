from enum import StrEnum, unique


@unique
class MilestoneStateEnum(StrEnum):
    OPEN = "open"
    CLOSED = "closed"
