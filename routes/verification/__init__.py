from fastapi import APIRouter
from .get import router as get_router

router = APIRouter(prefix="/keys")

router.include_router(get_router)
