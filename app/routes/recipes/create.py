from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.error import ApiError, InternalApiError
from app.repos.db import RecipeDB
from app.schemas.dto import RecipeCreate, RecipeOut
from app.schemas.error import ApiErrorResponse
from app.services.service import RecipeService
from app.shared.sqlite import get_db

router = APIRouter()

responses = {
    422: {"model": ApiErrorResponse, "description": "Validation error"},
    500: {"model": ApiErrorResponse, "description": "Internal error"},
}


@router.post("/", response_model=RecipeOut, status_code=201, responses=responses)
def create_recipe(payload: RecipeCreate, db: Session = Depends(get_db)):
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
        print(e)
        raise InternalApiError(e)
