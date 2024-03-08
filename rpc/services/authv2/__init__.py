from rpc.declaration.auth import auth_pb2_grpc
from .auth import AuthorizeInterface
from .getuser import GetUserInterface
from .getuservalidity import GetUserValidityInterface
from .searchuser import SearchUserInterface
from .sendpush import SendPushInterface


class AuthorizeServicerV2(auth_pb2_grpc.AuthServiceServicer):
    async def Authorize(self, request, context):
        return await AuthorizeInterface(self, request, context)
    
    async def GetUserValidity(self, request, context):
        return await GetUserValidityInterface(self, request, context)

    async def GetUser(self, request, context):
        return await GetUserInterface(self, request, context)
    
    async def SearchUser(self, request, context):
        return await SearchUserInterface(self, request, context)
    
    async def SendPush(self, request, context):
        return await SendPushInterface(self, request, context)
