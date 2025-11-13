from fastapi import APIRouter, Request

from app.schemas.dto import Health
from app.shared.db import check_db_health
from app.shared.limit import limiter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=Health)
@limiter.limit("5/minute")
def health(request: Request):
    db_status = check_db_health()
    return {"status": {"db": db_status}}
