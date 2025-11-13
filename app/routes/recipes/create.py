from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.models.error import ApiError, InternalApiError
from app.repos.db import RecipeDB
from app.schemas.dto import RecipeCreate, RecipeOut
from app.schemas.error import ApiErrorResponse
from app.services.service import RecipeService
from app.shared.db import get_db
from app.shared.limit import limiter

router = APIRouter()

responses = {
    422: {"model": ApiErrorResponse, "description": "Validation error"},
    429: {"model": ApiErrorResponse, "description": "Rate limit exceeded"},
    500: {"model": ApiErrorResponse, "description": "Internal error"},
}


@router.post("/", response_model=RecipeOut, status_code=201, responses=responses)
@limiter.limit("5/minute")
def create_recipe(request: Request, payload: RecipeCreate, db: Session = Depends(get_db)):
    try:
        repo = RecipeDB(db)
        service = RecipeService(repo)
        ingredients = [i.to_entity() for i in payload.ingredients]
        recipe = service.create_recipe(
            name=payload.name,
            ingredients=ingredients,
            total_time=payload.total_time,
            description=payload.description,
        )
        return RecipeOut.from_entity(recipe)
    except ApiError:
        raise
    except Exception as e:
        raise InternalApiError(e)
