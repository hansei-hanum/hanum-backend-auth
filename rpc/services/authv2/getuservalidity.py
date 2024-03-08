from database import User
from database import scope
from rpc.declaration.authv2.authv2_pb2 import (
    ValidateResult,
)


async def GetUserValidityInterface(self, request, context):
    async with scope() as sess:
        user = await sess.get(User, request.userid)

        if user:
            return ValidateResult(success=True)
        else:
            return ValidateResult(success=False)
