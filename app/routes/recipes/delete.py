from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models.error import ApiError, InternalApiError
from app.repos.db import RecipeDB
from app.schemas.error import ApiErrorResponse
from app.services.service import RecipeService
from app.shared.db import get_db
from app.shared.limit import limiter

router = APIRouter()

_responses = {
    404: {"model": ApiErrorResponse, "description": "Not found"},
    429: {"model": ApiErrorResponse, "description": "Rate limit exceeded"},
    500: {"model": ApiErrorResponse, "description": "Internal error"},
}


@router.delete("/{name}", status_code=204, responses=_responses)
@limiter.limit("5/minute")
def delete_recipe(request: Request, name: str, db: Session = Depends(get_db)):
    try:
        repo = RecipeDB(db)
        service = RecipeService(repo)
        service.delete_recipe(name)
        return JSONResponse(status_code=204, content=None)
    except ApiError:
        raise
    except Exception as e:
        raise InternalApiError(e)
