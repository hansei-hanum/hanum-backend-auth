from fastapi import Header
from fastapi.exceptions import HTTPException

from auth import AuthService


async def RequireAuth(authorization: str = Header(...)):
    try:
        token_type = authorization.split(" ")[0]
        token = authorization.split(" ")[1]

        if token_type != "Bearer":
            raise

        userid = await AuthService.authorize(token)
        if not userid:
            raise
        return userid
    except:
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")
