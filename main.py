from rpc import gRPCServer
import asyncio
from fastapi import FastAPI


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(gRPCServer.run())


@app.get("/")
async def root():
    return {"message": "Hello World"}
