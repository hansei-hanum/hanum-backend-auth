from fastapi import APIRouter
from .register import router as register_router
from .login import router as login_router
from .phone import router as phone_router

router = APIRouter(prefix="/auth")

router.include_router(register_router)
router.include_router(login_router)
router.include_router(phone_router)
