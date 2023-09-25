import asyncio
from concurrent.futures import ThreadPoolExecutor
from time import time
import grpc
from declaration.auth_pb2_grpc import AuthServiceStub
from declaration.auth_pb2 import AuthorizeRequest


async def get_user():
    channel = grpc.aio.insecure_channel(
        "ec2-52-78-121-2.ap-northeast-2.compute.amazonaws.com:50051"
    )

    client = AuthServiceStub(channel)

    start = time()
    for _ in range(500):
        if not (
            await client.Authorize(
                AuthorizeRequest(
                    token="MDAwMDAwMDAwMDAwMDAwMDAwMDE.MTY5MzU1Mjk0MQ.j892hz4yc0KnqLHMvNVBF7D573EoUCetb"
                )
            )
        ).success:
            print("FAIL")

    print((time() - start) / 2000)


with ThreadPoolExecutor(20) as pool:
    for _ in range(2):
        pool.submit(asyncio.run, get_user())
