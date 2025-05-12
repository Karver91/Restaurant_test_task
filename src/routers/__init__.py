from fastapi import APIRouter

from src.routers.table import router as table_router

router = APIRouter()

router.include_router(table_router)
