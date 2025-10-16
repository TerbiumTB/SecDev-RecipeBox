from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.infrastructure.db import RecipeRepo
from app.models.errors import ApiError, InternalApiError
from app.schemas.dto import RecipeCreate, RecipeOut, RecipeUpdate
from app.schemas.errors import ApiErrorResponse
from app.services.service import RecipeService

app = FastAPI(title="RecipeBox App", version="0.1.0")


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return exc.to_json()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    message = exc.detail if isinstance(exc.detail, str) else "http_error"

    err = ApiError(
        code="http_error",
        message=message,
        status_code=exc.status_code,
    )

    return err.to_json()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first = exc.errors()[0] if exc.errors() else {}
    message = first.get("msg", "validation error")

    err = ApiError(code="validation_error", message=message, status_code=422)

    return err.to_json()


@app.get("/health")
def health():
    return {"status": "ok"}


_repo = RecipeRepo()
_service = RecipeService(_repo)


@app.post(
    "/recipes",
    response_model=RecipeOut,
    status_code=201,
    responses={
        422: {"model": ApiErrorResponse, "description": "Validation error"},
        500: {"model": ApiErrorResponse, "description": "Internal error"},
    },
)
def create_recipe(payload: RecipeCreate):
    try:
        ingredients = [i.to_entity() for i in payload.ingredients]
        recipe = _service.create_recipe(
            name=payload.name,
            ingredients=ingredients,
            total_time=payload.total_time,
            description=payload.description,
        )
        return RecipeOut.from_entity(recipe)
    except ApiError:
        raise
    except Exception as e:
        print(e)
        raise InternalApiError(e)


@app.get("/recipes", response_model=list[RecipeOut])
def list_recipes():
    return [RecipeOut.from_entity(r) for r in _service.all_recipes()]


@app.get(
    "/recipes/{name}",
    response_model=RecipeOut,
    responses={
        404: {"model": ApiErrorResponse, "description": "Not found"},
        500: {"model": ApiErrorResponse, "description": "Internal error"},
    },
)
def get_recipe(name: str):
    try:
        r = _service.get_recipe_by_name(name)
        return RecipeOut.from_entity(r)
    except ApiError:
        raise
    except Exception as e:
        raise InternalApiError(e)


@app.patch(
    "/recipes/{name}",
    response_model=RecipeOut,
    responses={
        422: {"model": ApiErrorResponse, "description": "Validation error"},
        404: {"model": ApiErrorResponse, "description": "Not found"},
        500: {"model": ApiErrorResponse, "description": "Internal error"},
    },
)
def update_recipe(name: str, payload: RecipeUpdate):
    try:
        ingredients = None
        if payload.ingredients is not None:
            ingredients = [i.to_entity() for i in payload.ingredients]
        updated = _service.update_recipe(
            name=name,
            ingredients=ingredients,
            total_time=payload.total_time,
            description=payload.description,
        )
        return RecipeOut.from_entity(updated)
    except ApiError:
        raise
    except Exception as e:
        raise InternalApiError(e)


@app.delete(
    "/recipes/{name}",
    status_code=204,
    responses={
        404: {"model": ApiErrorResponse, "description": "Not found"},
        500: {"model": ApiErrorResponse, "description": "Internal error"},
    },
)
def delete_recipe(name: str):
    try:
        _service.delete_recipe(name)
        return JSONResponse(status_code=204, content=None)
    except ApiError:
        raise
    except Exception as e:
        raise InternalApiError(e)


# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema

#     openapi_schema = get_openapi(
#         title="RecipeBox API",
#         version="0.1.0",
#         routes=app.routes,
#     )

#     components = openapi_schema.get("components", {}).get("schemas", {})
#     for schema_name in ["HTTPValidationError", "ValidationError"]:
#         components[schema_name]["title"] = "Deprecated"
#         components.pop(schema_name, None)

#     # не знаю что здесь происходит, но это чтобы показывались только нужные ошибки в каждом методе
#     for path, methods in openapi_schema.get("paths", {}).items():
#         for method, operation in methods.items():
#             responses = operation.get("responses", {})
#             for status_code, response in list(responses.items()):
#                 content = response.get("content", {})
#                 for media_type, schema_obj in list(content.items()):
#                     schema_ref = schema_obj.get("schema", {}).get("$ref")
#                     if schema_ref and "HTTPValidationError" in schema_ref:
#                         # Удаляем полностью 422 ошибку или подменяем на твою
#                         responses.pop(status_code, None)

#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


# app.openapi = custom_openapi
