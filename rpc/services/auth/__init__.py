from ..declaration import auth_pb2_grpc
from .auth import AuthorizeInterface
from .getuser import GetUserInterface
from .sendpush import SendPushInterface


class AuthorizeServicer(auth_pb2_grpc.AuthServiceServicer):
    async def Authorize(self, request, context):
        return await AuthorizeInterface(self, request, context)

    async def GetUser(self, request, context):
        return await GetUserInterface(self, request, context)

    async def SendPush(self, request, context):
        return await SendPushInterface(self, request, context)
