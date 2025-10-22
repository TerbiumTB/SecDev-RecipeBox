from typing import Any

from fastapi import HTTPException
from fastapi.responses import JSONResponse


class ApiError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: dict[str, Any] = None,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}

    def to_dict(self) -> dict[str,]:
        error_data = {
            "error": {
                "code": self.code,
                "message": self.message,
            }
        }

        if self.details:
            error_data["error"]["details"] = self.details

        return error_data

    def to_json(self) -> JSONResponse:
        return JSONResponse(status_code=self.status_code, content=self.to_dict())

    def to_http_exception(self) -> HTTPException:
        return HTTPException(status_code=self.status_code, detail=self.to_dict())


class NotFoundApiError(ApiError):
    def __init__(self, message: str | Exception):
        super().__init__(
            code="not_found",
            message=str(message),
            status_code=404,
        )


class InternalApiError(ApiError):
    def __init__(self, message: str | Exception):
        super().__init__(code="internal_error", message=str(message), status_code=500)
