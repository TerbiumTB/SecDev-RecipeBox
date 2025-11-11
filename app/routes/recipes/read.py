from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.models.error import ApiError, InternalApiError
from app.repos.db import RecipeDB
from app.schemas.dto import RecipeOut
from app.schemas.error import ApiErrorResponse
from app.services.service import RecipeService
from app.shared.limit import limiter
from app.shared.sqlite import get_db

router = APIRouter()

_responses = {
    429: {"model": ApiErrorResponse, "description": "Rate limit exceeded"},
    500: {"model": ApiErrorResponse, "description": "Internal error"},
}


@router.get("/", response_model=list[RecipeOut], responses=_responses)
@limiter.limit("5/minute")
def read_recipes(request: Request, db: Session = Depends(get_db)):
    try:
        repo = RecipeDB(db)
        service = RecipeService(repo)
        return [RecipeOut.from_entity(r) for r in service.all_recipes()]
    except ApiError:
        raise
    except Exception as e:
        raise InternalApiError(e)


_responses = {
    404: {"model": ApiErrorResponse, "description": "Not found"},
    429: {"model": ApiErrorResponse, "description": "Rate limit exceeded"},
    500: {"model": ApiErrorResponse, "description": "Internal error"},
}


@router.get("/{name}", response_model=RecipeOut, responses=_responses)
@limiter.limit("5/minute")
def read_recipe(request: Request, name: str, db: Session = Depends(get_db)):
    try:
        repo = RecipeDB(db)
        service = RecipeService(repo)
        r = service.get_recipe_by_name(name)
        return RecipeOut.from_entity(r)
    except ApiError:
        raise
    except Exception as e:
        raise InternalApiError(e)
