from typing import Any
from uuid import uuid4

from fastapi import HTTPException
from fastapi.responses import JSONResponse


class ApiError(Exception):
    def __init__(
        self,
        type: str = "about:blank",
        title: str = "error",
        status: int = 400,
        detail: str | None = None,
        correlation_id: str | None = None,
        mask: bool = False,
        extensions: dict[str, Any] | None = None,
    ):
        super().__init__(detail or title)
        self.type = type
        self.title = title
        self.status = status
        self.detail = detail or title
        self.correlation_id = correlation_id or str(uuid4())
        self.mask = mask
        self.extensions = extensions

    def _mask_detail(self):
        if self.status >= 500:
            return "internal server error"
        return self.detail

    def to_problem(self) -> dict[str,]:
        detail = self._masked_detail() if self.mask else self.detail

        problem = {
            "type": self.type,
            "title": self.title,
            "status": self.status,
            "detail": detail,
            "instance": self.correlation_id,
        }

        if self.extensions:
            for k, v in self.extensions.items():
                if k in problem:
                    problem[f"x_{k}"] = v
                else:
                    problem[k] = v

        return problem

    def to_json(self) -> JSONResponse:
        return JSONResponse(status_code=self.status, content=self.to_problem())

    def to_http_exception(self) -> HTTPException:
        return HTTPException(status_code=self.status_code, detail=self.to_problem())


class ValidationApiError(ApiError):
    def __init__(
        self,
        detail: str = "validation error",
        extensions: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ):
        super().__init__(
            type="https://example.com/probs/validation",
            title="Validation Error",
            status=422,
            detail=detail,
            correlation_id=correlation_id,
            mask=False,
            extensions={"errors": extensions} if extensions else {},
        )


class NotFoundApiError(ApiError):
    def __init__(
        self,
        resource: str = "resource",
        identifier: Any = None,
        correlation_id: str | None = None,
    ):
        msg = f"{resource} not found" + (
            f": {identifier}" if identifier is not None else ""
        )
        super().__init__(
            type="https://example.com/probs/not-found",
            title="Not Found",
            status=404,
            detail=msg,
            correlation_id=correlation_id,
            mask=False,
        )


class InternalApiError(ApiError):
    def __init__(
        self, message: str = "internal error", correlation_id: str | None = None
    ):
        super().__init__(
            type="https://example.com/probs/internal",
            title="Internal Server Error",
            status=500,
            detail=message,
            correlation_id=correlation_id,
            mask=True,
        )


class HTTPApiError(ApiError):
    def __init__(
        self, message: str = "internal error", correlation_id: str | None = None
    ):
        super().__init__(
            type="https://example.com/probs/internal",
            title="Internal Server Error",
            status=500,
            detail=message,
            correlation_id=correlation_id,
            mask=False,
        )
