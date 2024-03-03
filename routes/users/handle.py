from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field
from database import User
from depends import RequireAuth
from services import UserService
from database import scope

router = APIRouter(prefix="/@me/handle")


class CreateHandleRequest(BaseModel):
    handle: str = Field(pattern=r"^[a-z0-9]{4,12}$")


@router.post("/")
async def create_handle(
    request: CreateHandleRequest, authid: int = Depends(RequireAuth)
):
    async with scope() as sess:
        user = await sess.get(User, authid)

        if not user:
            raise HTTPException(status_code=400, detail="USER_NOT_FOUND")

        async with UserService(sess, user) as service:
            result = await service.set_handle(request.handle)

            if result is False:
                raise HTTPException(status_code=403, detail="HANDLE_ALREADY_TAKEN")

            elif type(result) == float:
                return JSONResponse(
                    status_code=429,
                    content={
                        "message": "COOLDOWN_NOT_EXPIRED",
                        "data": {"retry_after": result},
                    },
                )

        return {"message": "SUCCESS", "data": None}
