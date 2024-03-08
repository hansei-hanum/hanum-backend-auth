from grpc import aio
from rpc.declaration.auth import auth_pb2_grpc
from rpc.declaration.authv2 import authv2_pb2_grpc
from rpc.services.auth import AuthorizeServicer
from rpc.services.authv2 import AuthorizeServicerV2
from env import gRPCEnv


class gRPCServer:
    @staticmethod
    async def run():
        server = aio.server()

        auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthorizeServicer(), server)
        authv2_pb2_grpc.add_AuthServiceV2Servicer_to_server(AuthorizeServicerV2(), server)

        server.add_insecure_port(f"[::]:{gRPCEnv.PORT}")
        await server.start()
        print("[GRPC] Server is running on port", gRPCEnv.PORT)
        await server.wait_for_termination()
