from fastapi import APIRouter

from src.routers.reservation import router as reservation_router
from src.routers.table import router as table_router

router = APIRouter()

router.include_router(reservation_router)
router.include_router(table_router)
