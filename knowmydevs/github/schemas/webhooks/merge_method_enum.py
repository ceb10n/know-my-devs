from enum import StrEnum, unique


@unique
class MergeMethodEnum(StrEnum):
    MERGE = "merge"
    SQUASH = "squash"
    REBASE = "rebase"
