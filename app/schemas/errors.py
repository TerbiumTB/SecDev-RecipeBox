from typing import Any

from pydantic import BaseModel

# from app.models.errors import ApiError


class ApiErrorResponse(BaseModel):
    code: str
    message: str
    details: dict[str, Any]
