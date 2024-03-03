from fastapi import APIRouter
from .getuser import router as getuser_router
from .verify import router as verify_router
from .delete import router as delete_router
from .handle import router as handle_router

router = APIRouter(prefix="/users")

router.include_router(getuser_router)
router.include_router(verify_router)
router.include_router(delete_router)
router.include_router(handle_router)
