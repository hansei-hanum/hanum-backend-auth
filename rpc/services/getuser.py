from ..declaration.auth_pb2 import (
    Verification as VerificationMessage,
    User as UserMessage,
    GetUserResult,
)
from database import scope, User
from services import UserService


async def GetUserInterface(self, request, context):
    async with scope() as session:
        user: User | None = await session.get(User, request.userid)

        if not user:
            return GetUserResult(success=False)

        async with UserService(session, user) as service:
            verification = await service.get_verification()

            return GetUserResult(
                success=True,
                user=UserMessage(
                    id=user.id,
                    phone=user.phone,
                    name=user.name,
                    profile=user.profile,
                    created_at=str(user.created_at),
                    is_suspended=(await service.is_suspended()),
                    verification=VerificationMessage(
                        type=verification.type,
                        department=verification.department,
                        grade=verification.grade,
                        classroom=verification.classroom,
                        number=verification.number,
                        valid_until=str(verification.valid_until),
                        graduated_at=verification.graduated_at,
                    )
                    if verification is not None
                    else None,
                ),
            )
