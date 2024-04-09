import base64
import hashlib
import hmac
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
import time
import aiohttp
from urllib.parse import urlparse
from env import SENSEnv


# class SMSSender:
#     def __init__(self):
#         self.access_key = SENSEnv.ACCESS_KEY
#         self.secret_key = SENSEnv.SECRET_KEY
#         self.service_id = SENSEnv.SERVICE_ID
#         self.phone_number = SENSEnv.PHONE_NUMBER

#     def signature(self, method: str, path: str):
#         timestamp = int(time.time() * 1000)
#         return timestamp, base64.b64encode(
#             hmac.new(
#                 self.secret_key.encode("utf-8"),
#                 f"{method} {path}\n{timestamp}\n{self.access_key}".encode("utf-8"),
#                 digestmod=hashlib.sha256,
#             ).digest()
#         ).decode("utf-8")

#     async def send(self, to: str, message: str):
#         url = urlparse(
#             "https://api.coolsms.co.kr/messages/"
#             + self.service_id
#             + "/messages"
#         )
#         timestamp, signature = self.signature("POST", url.path)

#         async with aiohttp.ClientSession() as session:
#             async with session.post(
#                 url.geturl(),
#                 headers={
#                     "Content-Type": "application/json; charset=utf-8",
#                     "x-ncp-apigw-timestamp": str(timestamp),
#                     "x-ncp-iam-access-key": self.access_key,
#                     "x-ncp-apigw-signature-v2": signature,
#                 },
#                 json={
#                     "type": "SMS",
#                     "from": self.phone_number,
#                     "content": message,
#                     "messages": [{"to": to}],
#                 },
#             ) as response:
#                 response.raise_for_status()


class SMSSender:
    def __init__(self):
        self.access_key = SENSEnv.ACCESS_KEY
        self.secret_key = SENSEnv.SECRET_KEY
        self.service_id = SENSEnv.SERVICE_ID
        self.phone_number = SENSEnv.PHONE_NUMBER
        self.sms_salt = SENSEnv.SMS_SALT
        

    def signature(self, method: str, path: str):
        timestamp = int(time.time() * 1000)
        return timestamp, base64.b64encode(
            hmac.new(
                self.secret_key.encode("utf-8"),
                f"{method} {path}\n{timestamp}\n{self.access_key}".encode("utf-8"),
                digestmod=hashlib.sha256,
            ).digest()
        ).decode("utf-8")
    
    async def send(self, to: str, message: str):
        url = "http://api.coolsms.co.kr/messages/v4/send"
        timestamp = int(time.time() * 1000)
        headers = {
            "Authorization": f"HMAC-SHA256 apiKey={self.access_key}, date={timestamp}, salt={self.sms_salt}, signature={self.signature('POST', url)[1]}",
            "Content-Type": "application/json"
        }
        data = f'{{"message":{{"to":"{to}","from":"{self.phone_number}","text":"{message}","type":"SMS"}}}}'

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                status_code = response.status
                text = await response.text()
                print(status_code)
                print(text)

