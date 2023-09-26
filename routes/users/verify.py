from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from database import User, VerificationKey, scope
from depends import RequireAuth
from pydantic import BaseModel

router = APIRouter()


class VerificationRequest(BaseModel):
    code: str


@router.post("/@me/verifications")
async def get_user(req: VerificationRequest, authid: int = Depends(RequireAuth)):
    async with scope() as sess:
        user = await sess.execute(select(User).where(User.id == authid))
        user = user.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

        key: VerificationKey = await sess.get(VerificationKey, req.code)

        if not key:
            raise HTTPException(status_code=404, detail="KEY_NOT_FOUND")

        if key.user_id:
            raise HTTPException(status_code=409, detail="KEY_ALREADY_USED")

        if key.valid_until is not None and key.valid_until < datetime.now():
            raise HTTPException(status_code=409, detail="KEY_EXPIRED")

        key.user_id = user.id
        await sess.commit()

        return {"message": "SUCCESS", "data": None}
