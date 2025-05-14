from typing import Literal, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import PhoneAuth
from auth import AuthService
from database import User, scope
from sqlalchemy import select
from fastapi_limiter.depends import RateLimiter
from fastapi.exceptions import HTTPException
from services import UserService
from env import Env, AuthEnv
import jwt, utils

router = APIRouter(prefix="/login")


class LoginRequest(BaseModel):
    phone: str
    code: str
    type: Optional[Literal["hanum", "sports"]] = "hanum"


@router.post("/", dependencies=[Depends(RateLimiter(times=10, minutes=30))])
async def login(request: LoginRequest):
    async with scope() as session:
        user = (
            await session.execute(select(User).where(User.phone == request.phone))
        ).scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

        if request.type == "sports":
            token = jwt.encode(
                {
                    "id": user.id,
                    "name": user.name,
                    "validationString": "Unknown",
                },
                (AuthEnv.EXTERNAL_SERVICE_JWT_SECRET + request.type),
            )
            return {"message": "SUCCESS", "data": token}

        if not (Env.DEBUG or request.phone in Env.TEST_PHONE_NUMBERS):
            if not (await PhoneAuth.verify(request.phone, request.code)):
                raise HTTPException(status_code=401, detail="INVALID_VERIFICATION_CODE")

        async with UserService(session, user) as service:
            if request.type == "hanum":
                if await service.is_suspended():
                    raise HTTPException(status_code=403, detail="ACCOUNT_SUSPENDED")

                token = await AuthService.issue_token(user.id)
            else:
                token = jwt.encode(
                    {
                        "id": user.id,
                        "name": user.name,
                        "validationString": utils.get_userinfo_string(
                            await service.get_verification()
                        ),
                    },
                    (AuthEnv.EXTERNAL_SERVICE_JWT_SECRET + request.type),
                )

    return {"message": "SUCCESS", "data": token}
