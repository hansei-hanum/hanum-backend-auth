from fastapi import FastAPI, HTTPException, Request, Response
from database import Base, engine
from routes import include_router
import redis.asyncio as redis
from env import RedisEnv
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from env import Env
from utils import random_string
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        {"message": exc.detail, "data": None}, status_code=exc.status_code
    )


async def default_callback(request: Request, response: Response, pexpire: int):
    raise HTTPException(429, "RATE_LIMITED")


async def default_identifier(request: Request):
    # if not Env.DEBUG:
    #     forwarded = request.headers.get("X-Forwarded-For")
    #     if forwarded:
    #         return forwarded.split(",")[0]
    #     return request.client.host + ":" + request.scope["path"]

    return f"DEBUG_{random_string(32)}"


@app.on_event("startup")
async def startup_event():
    redis_session = redis.Redis(
        host=RedisEnv.HOST, port=RedisEnv.PORT, db=RedisEnv.RATE_LIMITER_DB
    )
    await FastAPILimiter.init(
        redis_session, identifier=default_identifier, http_callback=default_callback
    )

    async with engine.begin() as sess:
        await sess.run_sync(Base.metadata.create_all)


include_router(app)
