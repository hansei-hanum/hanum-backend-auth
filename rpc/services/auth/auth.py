from auth import AuthService
from ..declaration.auth_pb2 import (
    AuthorizeResult,
)


async def AuthorizeInterface(self, request, context):
    result = await AuthService.authorize(request.token)
    if result:
        return AuthorizeResult(success=True, userid=result)
    else:
        return AuthorizeResult(success=False)
