from fastapi import APIRouter

from .discussions import router as discussions_router
from .prs import router as prs_router
from .stats import router as stats_router
from .webhooks import router as webhooks_router

router = APIRouter(prefix="/v1")
router.include_router(discussions_router)
router.include_router(prs_router)
router.include_router(stats_router)
router.include_router(webhooks_router)
