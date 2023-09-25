from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from database import User
from depends import RequireAuth
from services import UserService
from database import scope

router = APIRouter(prefix="/{userid}")


@router.get("/")
async def get_user(userid: int | str, authid: int = Depends(RequireAuth)):
    include_sensitive = False
    if userid == "@me":
        userid = authid
        include_sensitive = True

    async with scope() as sess:
        user = await sess.get(User, userid)

        if not user:
            raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

        async with UserService(sess, user) as service:
            return {
                "message": "SUCCESS",
                "data": await service.serialize(include_sensitive=include_sensitive),
            }
