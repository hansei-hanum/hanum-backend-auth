from .smssender import SMSSender
import redis.asyncio as redis
import utils
from env import RedisEnv

connection = redis.Redis(
    host=RedisEnv.HOST, port=RedisEnv.PORT, db=RedisEnv.PHONE_VERIFICATION_DB
)


class PhoneAuth:
    @staticmethod
    async def send(phone: str):
        verification_key = utils.random_number(6)
        await connection.set(phone, verification_key, ex=300)
        await SMSSender().sendMessage(
            phone, f"[한움] 인증번호는 {verification_key}입니다. 5분 내에 입력해주세요."
        )

    @staticmethod
    async def verify(phone: str, verification_key: str) -> bool:
        correct_code = await connection.get(phone)

        if not correct_code:
            return False

        if (correct_code).decode() == verification_key:
            await connection.delete(phone)
            return True
        else:
            return False
