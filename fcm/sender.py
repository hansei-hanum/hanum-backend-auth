import aiohttp
from . import gauth
from env import FirebaseEnv


class FCMSender:
    def __init__(self, topic: str | None = None, token: str | None = None):
        if not (topic or token):
            raise ValueError("topic or token must be specified")
        if topic and token:
            raise ValueError("topic and token cannot be specified at the same time")

        self.target = topic or token
        self.is_topic = bool(topic)

    async def send(self, title: str, body: str, image: str, deeplink: str):
        if not body:
            raise ValueError("body must be specified")

        json_data = {
            "message": {
                "topic" if self.is_topic else "token": self.target,
                "notification": {
                    "title": title,
                    "body": body,
                    "image": image,
                },
                "data": {
                    "url": deeplink,
                },
                "android": {
                    "priority": "high",
                },
            }
        }

        return await self._request(json_data)

    async def _request(self, json_data: dict):
        token = await gauth.get_access_token()
        async with aiohttp.ClientSession() as sess:
            response = await sess.post(
                f"https://fcm.googleapis.com/v1/projects/{FirebaseEnv.PROJECT_ID}/messages:send",
                json=json_data,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
            )

            return response.status
