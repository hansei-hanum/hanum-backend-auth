from fastapi import APIRouter, Depends
from pydantic import BaseModel, validator
from depends import RequireAuth
from database import scope, FCMToken, User
from sqlalchemy import select, delete, insert


router = APIRouter(prefix="/tokens/fcm")


class FCMTokenRequest(BaseModel):
    token: str
    platform: str

    @validator("platform")
    def validate_platform(cls, v):
        if v not in ["IOS", "ANDROID"]:
            raise ValueError("platform must be IOS or ANDROID")
        return v


@router.post("/")
async def update_fcm_token(request: FCMTokenRequest, userid=Depends(RequireAuth)):
    async with scope() as session:
        user: User = await session.get(User, userid)

        if not user:
            return {"message": "USER_NOT_FOUND", "data": None}

        await session.execute(delete(FCMToken).where(FCMToken.user_id == userid))
        await session.execute(
            insert(FCMToken).values(
                user_id=userid, token=request.token, platform=request.platform
            )
        )
        await session.commit()

    return {"message": "SUCCESS", "data": None}


@router.delete("/")
async def delete_fcm_token(userid=Depends(RequireAuth)):
    async with scope() as session:
        user: User = await session.get(User, userid)

        if not user:
            return {"message": "USER_NOT_FOUND", "data": None}

        await session.execute(delete(FCMToken).where(FCMToken.user_id == userid))
        await session.commit()

    return {"message": "SUCCESS", "data": None}
