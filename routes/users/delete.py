from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from database import User
from depends import RequireAuth
from services import UserService
from auth import AuthService
from database import scope

router = APIRouter(prefix="/@me")


@router.delete("/")
async def delete_user(userid: int = Depends(RequireAuth)):
    async with scope() as sess:
        user = await sess.get(User, userid)

        if not user:
            raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

        async with UserService(sess, user) as service:
            await service.delete()

        await AuthService.revoke_token(userid)

        return {"message": "SUCCESS", "data": None}
