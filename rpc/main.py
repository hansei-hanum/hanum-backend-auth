from grpc import aio
from .declaration import auth_pb2_grpc
from .services import AuthorizeServicer
from env import gRPCEnv


class gRPCServer:
    @staticmethod
    async def run():
        server = aio.server()
        gRPCEnv.include(server)
        server.add_insecure_port(f"[::]:{gRPCEnv.PORT}")
        await server.start()
        await server.wait_for_termination()

    async def include(server):
        auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthorizeServicer(), server)
