from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import case, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from database import User
from database.user import UserSuspention
from typing import Literal, NamedTuple

from database.verification import VerificationKey


class UserVerification(NamedTuple):
    type: Literal["STUDENT", "TEACHER", "GRADUATED"]
    department: Literal[
        "CLOUD_SECURITY",
        "NETWORK_SECURITY",
        "HACKING_SECURITY",
        "METAVERSE_GAME",
        "GAME",
    ] | None = None
    grade: int | None = None
    classroom: int | None = None
    number: int | None = None
    valid_until: datetime | None = None
    graduated_at: datetime | None = None


class UserService:
    def __init__(self, sess: AsyncSession, user: User):
        self.sess: AsyncSession = sess
        self.user: User = user

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            await self.sess.rollback()
        else:
            await self.sess.commit()

    async def suspend(self, reason: str, duration: timedelta) -> None:
        await self.sess.add(
            UserSuspention(
                user_id=self.user.id, reason=reason, expiry=datetime.now() + duration
            )
        )

    async def is_suspended(self) -> bool:
        return (
            await self.sess.execute(
                select(UserSuspention)
                .where(UserSuspention.user_id == self.user.id)
                .where(UserSuspention.expiry > datetime.now())
            )
        ).scalar_one_or_none() is not None

    async def get_verification(self):
        valid_key: VerificationKey | None = (
            await self.sess.execute(
                select(VerificationKey)
                .filter(VerificationKey.user_id == self.user.id)
                .order_by(
                    case((VerificationKey.valid_until == None, 0), else_=1),
                    VerificationKey.valid_until.desc(),
                )
                .limit(1)
            )
        ).scalar_one_or_none()

        if valid_key is None:
            return None

        if valid_key.valid_until and valid_key.valid_until < datetime.now():
            if not valid_key.type == "STUDENT":
                return None

            if not valid_key.grade == 3:
                return None

            if not valid_key.created_at.year < datetime.now().year:
                return None

            return UserVerification(
                type="GRADUATED",
                department=valid_key.department,
                graduated_at=str(valid_key.created_at.year + 1),
            )

        return UserVerification(
            type=valid_key.type,
            department=valid_key.department,
            grade=valid_key.grade,
            classroom=valid_key.classroom,
            number=valid_key.number,
            valid_until=valid_key.valid_until,
        )

    async def serialize(self, include_sensitive: bool) -> dict:
        verification = await self.get_verification()

        data = {}
        data["id"] = self.user.id
        if include_sensitive:
            data["phone"] = self.user.phone
        data["name"] = self.user.name
        data["profile"] = self.user.profile
        data["created_at"] = self.user.created_at.isoformat()
        data["verification"] = verification._asdict() if verification else None

        return data

    async def delete(self) -> None:
        await self.sess.delete(self.user)
