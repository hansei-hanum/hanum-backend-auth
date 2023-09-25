from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import PhoneAuth
from auth import AuthService
from database import User, scope
from sqlalchemy import select
from fastapi_limiter.depends import RateLimiter
from fastapi.exceptions import HTTPException
from services import UserService
from env import Env

router = APIRouter(prefix="/login")


class LoginRequest(BaseModel):
    phone: str
    code: str


@router.post("/", dependencies=[Depends(RateLimiter(times=10, minutes=30))])
async def login(request: LoginRequest):
    async with scope() as session:
        user = (
            await session.execute(select(User).where(User.phone == request.phone))
        ).scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

        if not Env.DEBUG:
            if not (await PhoneAuth.verify(request.phone, request.code)):
                raise HTTPException(status_code=401, detail="INVALID_VERIFICATION_CODE")

        async with UserService(session, user) as service:
            if await service.is_suspended():
                raise HTTPException(status_code=403, detail="ACCOUNT_SUSPENDED")

            token = await AuthService.issue_token(user.id)

    return {"message": "SUCCESS", "data": token}
