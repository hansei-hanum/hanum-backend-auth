from fastapi import APIRouter, Depends
from depends import RequireAuth
from dataclasses import dataclass
from jose import jwt
from datetime import datetime, timedelta

from utils.tokens import create_access_token
from database.DTO.Response import JwtPayloadResponse

router = APIRouter()

SECRET_KEY = "your_secret_key" 
ALGORITHM = "HS256"



@router.get("/jwt_enc")
async def jwt_enc(token: str = Depends(RequireAuth)):
    user = JwtPayloadResponse(id=1, name="John Doe", verification="클라우드 보안과 2반 8번")
    access_token = create_access_token(user)
    return {"access_token": access_token}