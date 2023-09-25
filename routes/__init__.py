from fastapi import FastAPI
from .auth import router as auth_router
from .users import router as users_router
from .verification import router as verification_router
from .notification import router as notification_router


def include_router(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(verification_router)
    app.include_router(notification_router)
