from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.models.error import ApiError, ValidationApiError
from app.routes.recipes import route as recipes_route
from app.shared.limit import limiter, rate_limit_exceeded

app = FastAPI(title="RecipeBox App", version="0.1.0")
app.include_router(recipes_route.router)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded)
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return exc.to_json()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    message = exc.detail if isinstance(exc.detail, str) else "http_error"
    err = ApiError(title="HTTP Error", status=exc.status_code, details=message)
    # err = ApiError(
    #     code="http_error",
    #     message=message,
    #     status_code=exc.status_code,
    # )

    return err.to_json()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # extensions = exc.errors() if exc.errors() else {}
    # message = first.get("msg", "validation error")
    err = ValidationApiError(detail="pydantic error", extensions=exc.errors())
    # err = ApiError(code="validation_error", message=message, status_code=422)

    return err.to_json()


@app.get("/health")
def health():
    return {"status": "ok"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="RecipeBox API",
        version="0.1.0",
        routes=app.routes,
    )

    components = openapi_schema.get("components", {}).get("schemas", {})
    for schema_name in ["HTTPValidationError", "ValidationError"]:
        components[schema_name]["title"] = "Deprecated"
        components.pop(schema_name, None)

    # не знаю что здесь происходит, но это чтобы показывались только нужные ошибки в каждом методе
    for path, methods in openapi_schema.get("paths", {}).items():
        for method, operation in methods.items():
            responses = operation.get("responses", {})
            for status_code, response in list(responses.items()):
                content = response.get("content", {})
                for media_type, schema_obj in list(content.items()):
                    schema_ref = schema_obj.get("schema", {}).get("$ref")
                    if schema_ref and "HTTPValidationError" in schema_ref:
                        responses.pop(status_code, None)

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
