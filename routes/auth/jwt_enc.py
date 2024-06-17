from fastapi import APIRouter, Depends
from depends import RequireAuth

from utils.tokens import create_access_token
from services.user import UserService

router = APIRouter()





@router.get("/jwt_enc")
async def jwt_enc(token: str = Depends(RequireAuth)):
    user = UserService(id=1, name="John Doe", verification="클라우드 보안과 2반 8번")
    access_token = create_access_token(user)
    return {"access_token": access_token}