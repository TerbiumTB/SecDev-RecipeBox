# from fastapi import FastAPI, HTTPException, Request
from fastapi import APIRouter

from . import create, delete, read, update

router = APIRouter(prefix="/recipes", tags=["Recipes"])
router.include_router(create.router)
router.include_router(read.router)
router.include_router(update.router)
router.include_router(delete.router)
