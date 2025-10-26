from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from app.models.error import ApiError

limiter = Limiter(key_func=get_remote_address)


@limiter.limit("5/minute")
def rate_limit_exceeded(request: Request, exc):
    client_ip = request.client.host

    if client_ip in ("127.0.0.1", "::1"):
        return None

    err = ApiError(
        type="rate_limit_exceeded",
        title="Too Many Requests",
        status=429,
        detail="Rate limit exceeded. Try again later.",
    )
    raise err.to_problem()
