from fastapi import APIRouter

from .v1 import routers

router = APIRouter()
router.include_router(routers.router)
