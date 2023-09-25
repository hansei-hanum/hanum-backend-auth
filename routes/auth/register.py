from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import PhoneAuth
from auth import AuthService
from database import User, scope
from sqlalchemy import select
from fastapi_limiter.depends import RateLimiter
from fastapi.exceptions import HTTPException
from env import Env

router = APIRouter(prefix="/register")


class RegisterRequest(BaseModel):
    phone: str
    code: str
    name: str


@router.post("/", dependencies=[Depends(RateLimiter(times=5, minutes=30))])
async def register(request: RegisterRequest):
    async with scope() as session:
        user = (
            await session.execute(select(User).where(User.phone == request.phone))
        ).scalar_one_or_none()

        if user:
            raise HTTPException(status_code=409, detail="ALREADY_REGISTERED")

        if not (Env.DEBUG or request.phone in Env.TEST_PHONE_NUMBERS):
            if not (await PhoneAuth.verify(request.phone, request.code)):
                raise HTTPException(status_code=401, detail="INVALID_VERIFICATION_CODE")

        new_user = User(phone=request.phone, name=request.name)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        token = await AuthService.issue_token(new_user.id)

    return {"message": "SUCCESS", "data": token}
