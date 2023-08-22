from ..declaration.auth_pb2 import AuthorizeRequest, AuthorizeResult, AuthError
from ..declaration import auth_pb2_grpc


class AuthorizeServicer(auth_pb2_grpc.AuthServiceServicer):
    async def Authorize(self, request, context):
        if request.token == "test":
            return AuthorizeResult(success=True)
        return AuthorizeResult(success=False, error=AuthError.INVAILD_TOKEN)
