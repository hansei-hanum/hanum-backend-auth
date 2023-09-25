from fastapi import APIRouter, Depends
from pydantic import BaseModel, validator
from auth import PhoneAuth
from fastapi_limiter.depends import RateLimiter
from fastapi.exceptions import HTTPException
from env import Env
import re

router = APIRouter(prefix="/phone")


class PhoneRequest(BaseModel):
    phone: str

    @validator("phone")
    def phone_validator(cls, v):
        if not re.match(r"^010-?\d{4}-?\d{4}$", v):
            raise ValueError("휴대전화번호가 잘못되었습니다.")
        return v


@router.post("/", dependencies=[Depends(RateLimiter(times=5, minutes=30))])
async def request_phone(request: PhoneRequest):
    if Env.DEBUG or request.phone in Env.TEST_PHONE_NUMBERS:
        return {"message": "SUCCESS", "data": None}

    try:
        await PhoneAuth.send(request.phone)
    except:
        raise HTTPException(status_code=500, detail="EXTERNAL_API_EXCEPTION")

    return {"message": "SUCCESS", "data": None}
