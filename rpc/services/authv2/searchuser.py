from database import User
from database import scope
from sqlalchemy import select
from services import UserService
from rpc.declaration.authv2.authv2_pb2 import (
    SearchUserResult,
    User as UserMessage,
    Verification as VerificationMessage,
)
import traceback


async def SearchUserInterface(self, request, context):
    try:
        async with scope() as sess:
            query = request.query

            if not query:
                return SearchUserResult(users=[])

            stmt = select(User.id).where(User.name.like(f"%{query}%"))
            user_ids = [userid for userid in (await sess.execute(stmt)).scalars().all()]

            user_list = []

            for user_id in user_ids:
                user: User | None = await sess.get(User, user_id)
                async with UserService(sess, user) as service:
                    verification = await service.get_verification()

                    user_list.append(
                        UserMessage(
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
                        )
                    )

            return SearchUserResult(users=user_list)
        
    except Exception as e:
        traceback.print_exc()
