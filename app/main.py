from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.dto.dto import RecipeCreate, RecipeOut, RecipeUpdate
from app.infrastructure.db import RecipeRepo
from app.services.service import RecipeService

app = FastAPI(title="RecipeBox App", version="0.1.0")


class ApiError(Exception):
    def __init__(self, code: str, message: str, status: int = 400):
        self.code = code
        self.message = message
        self.status = status


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, str) else "http_error"
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": "http_error", "message": detail}},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first = exc.errors()[0] if exc.errors() else {}
    msg = first.get("msg", "validation error")
    return JSONResponse(
        status_code=422, content={"error": {"code": "validation_error", "message": msg}}
    )


@app.get("/health")
def health():
    return {"status": "ok"}


_repo = RecipeRepo()
_service = RecipeService(_repo)


@app.post("/recipes", response_model=RecipeOut, status_code=201)
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
    except ValueError as e:
        raise ApiError(code="conflict", message=str(e), status=409)
    except Exception as e:
        raise ApiError(code="internal_error", message=str(e), status=500)


@app.get("/recipes", response_model=list[RecipeOut])
def list_recipes():
    return [RecipeOut.from_entity(r) for r in _service.all_recipes()]


@app.get("/recipes/{name}", response_model=RecipeOut)
def get_recipe(name: str):
    try:
        r = _service.get_recipe_by_name(name)
        return RecipeOut.from_entity(r)
    except KeyError:
        raise ApiError(code="not_found", message="recipe not found", status=404)
    except Exception as e:
        raise ApiError(code="internal_error", message=str(e), status=500)


@app.put("/recipes/{name}", response_model=RecipeOut)
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
    except KeyError:
        raise ApiError(code="not_found", message="recipe not found", status=404)
    except Exception as e:
        raise ApiError(code="internal_error", message=str(e), status=500)


@app.delete("/recipes/{name}", status_code=204)
def delete_recipe(name: str):
    try:
        _service.delete_recipe(name)
        return JSONResponse(status_code=204, content=None)
    except KeyError:
        raise ApiError(code="not_found", message="recipe not found", status=404)
    except Exception as e:
        raise ApiError(code="internal_error", message=str(e), status=500)
