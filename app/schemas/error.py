from typing import Any

from pydantic import BaseModel


class ApiErrorResponse(BaseModel):
    type: str
    title: str
    status: int
    detail: str | None
    correlation_id: str | None
    mask: bool
    extensions: dict[str, Any] | None
