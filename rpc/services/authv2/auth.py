from auth import AuthService
from rpc.declaration.authv2.authv2_pb2 import (
    AuthorizeResult,
)


async def AuthorizeInterface(self, request, context):
    result = await AuthService.authorize(request.token)
    if result:
        return AuthorizeResult(success=True, userid=result)
    else:
        return AuthorizeResult(success=False)
