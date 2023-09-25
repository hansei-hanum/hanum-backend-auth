from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from database import VerificationKey
from fastapi_limiter.depends import RateLimiter
from depends import RequireAuth
from database import scope

router = APIRouter(prefix="/{key}")


@router.get("/", dependencies=[Depends(RateLimiter(times=10, minutes=30))])
async def check_key(key: str, authid: int = Depends(RequireAuth)):
    async with scope() as sess:
        key: VerificationKey = await sess.get(VerificationKey, key)

        if not key:
            raise HTTPException(status_code=404, detail="KEY_NOT_FOUND")

        return {
            "message": "SUCCESS",
            "data": {
                "type": key.type,
                "department": key.department,
                "grade": key.grade,
                "classroom": key.classroom,
                "number": key.number,
                "isUsed": key.user_id is not None,
            },
        }
