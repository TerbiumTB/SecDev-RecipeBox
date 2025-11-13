from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.models.error import ApiError, InternalApiError
from app.repos.db import RecipeDB
from app.schemas.dto import RecipeOut, RecipeUpdate
from app.schemas.error import ApiErrorResponse
from app.services.service import RecipeService
from app.shared.db import get_db
from app.shared.limit import limiter

router = APIRouter()

_responses = {
    422: {"model": ApiErrorResponse, "description": "Validation error"},
    404: {"model": ApiErrorResponse, "description": "Not found"},
    429: {"model": ApiErrorResponse, "description": "Rate limit exceeded"},
    500: {"model": ApiErrorResponse, "description": "Internal error"},
}


@router.patch("/{name}", response_model=RecipeOut, responses=_responses)
@limiter.limit("5/minute")
def update_recipe(
    request: Request, name: str, payload: RecipeUpdate, db: Session = Depends(get_db)
):
    try:
        repo = RecipeDB(db)
        service = RecipeService(repo)
        ingredients = None

        if payload.ingredients is not None:
            ingredients = [i.to_entity() for i in payload.ingredients]

        updated = service.update_recipe(
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
