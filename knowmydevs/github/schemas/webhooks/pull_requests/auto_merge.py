from pydantic import BaseModel

from knowmydevs.github.schemas.webhooks import MergeMethodEnum, User


class AutoMerge(BaseModel):
    enabled_by: User
    merge_method: MergeMethodEnum
    commit_title: str
    commit_message: str
