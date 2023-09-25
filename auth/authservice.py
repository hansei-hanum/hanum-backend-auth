import redis.asyncio as redis
from unpaddedbase64 import encode_base64, decode_base64
import utils
import time
from env import RedisEnv

connection = redis.Redis(
    host=RedisEnv.HOST, port=RedisEnv.PORT, db=RedisEnv.SESSION_MANAGER_DB
)


class AuthService:
    @staticmethod
    async def authorize(token: str) -> int | None:
        try:
            user_id = int(decode_base64(token.split(".")[0]).decode())
            real_token = (await connection.get(user_id)).decode()
        except:
            return None

        return user_id if token == real_token else None

    @staticmethod
    async def issue_token(user_id: int) -> str:
        user = encode_base64(str(user_id).zfill(20).encode())
        timestamp = encode_base64(str(int(time.time())).encode())
        random = utils.random_string(32)

        token = f"{user}.{timestamp}.{random}"

        await connection.set(str(user_id), token)

        return token

    @staticmethod
    async def revoke_token(user_id: int) -> None:
        await connection.delete(str(user_id))
