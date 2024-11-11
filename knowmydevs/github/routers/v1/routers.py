from fastapi import APIRouter

from .webhooks import router as webhooks_router

router = APIRouter(prefix="/v1")
router.include_router(webhooks_router)
