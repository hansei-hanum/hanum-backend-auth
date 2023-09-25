from fastapi import APIRouter
from .managetoken import router as managetoken_router

router = APIRouter(prefix="/users/@me")
router.include_router(managetoken_router)
