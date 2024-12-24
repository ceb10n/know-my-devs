from typing import Any, TypedDict


class Metadata(TypedDict):
    summary: str
    description: str
    operation_id: str
    responses: dict[str | int, dict[str, Any]]
    status_code: int | None = None
