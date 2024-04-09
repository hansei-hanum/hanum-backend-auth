import base64
import hashlib
import hmac
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
import time
import aiohttp
from urllib.parse import urlparse
from env import SENSEnv
import sys

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
        self.api_access_key = SENSEnv.ACCESS_KEY
        self.secret_key = SENSEnv.SECRET_KEY
        self.service_id = SENSEnv.SERVICE_ID
        self.phone_number = SENSEnv.PHONE_NUMBER
        self.sms_salt = SENSEnv.SMS_SALT
        

    # def signature(self, method: str, path: str):
    #     timestamp = int(time.time() * 1000)
    #     return timestamp, base64.b64encode(
    #         hmac.new(
    #             self.secret_key.encode("utf-8"),
    #             f"{method} {path}\n{timestamp}\n{self.access_key}".encode("utf-8"),
    #             digestmod=hashlib.sha256,
    #         ).digest()
    #     ).decode("utf-8")
    
    async def sendMessage(self, to: str, message: str):
        # url = "http://api.coolsms.co.kr/messages/v4/send"
        # timestamp = int(time.time() * 1000)

        params = dict()
        params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
        params['to'] = f'{to}' # Recipients Number '01000000000,01000000001'
        params['from'] = f'{self.phone_number}' # Sender number
        params['text'] = f'{message}' # Message

        # headers = {
        #     "Authorization": f"HMAC-SHA256 apiKey={self.access_key}, date={timestamp}, salt={self.sms_salt}, signature={self.signature('POST', url)[1]}",
        #     "Content-Type": "application/json"
        # }
        # data = f'{{"message":{{"to":"{to}","from":"{self.phone_number}","text":"{message}","type":"SMS"}}}}'

        access_key = self.api_access_key
        secret_key = self.secret_key

        cool = Message(access_key, secret_key)

        try:
            response = cool.send(params)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])

            if "error_list" in response:
                print("Error List : %s" % response['error_list'])

        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)

        # async with aiohttp.ClientSession() as session:
        #     async with session.post(url, headers=headers, data=data) as response:
        #         status_code = response.status
        #         # text = await response.text()
        #         text = cool.send(message)
        #         print(f"Response Status: {status_code}")
        #         print(f"Response Body: {text}")
        #         if status_code != 200:
        #             raise CoolsmsException(status_code, "Failed to send SMS.")
                
                # try:
                #     response = cool.send(message)
                #     print("Success Count : %s" % response['success_count'])
                #     print("Error Count : %s" % response['error_count'])
                #     print("Group ID : %s" % response['group_id'])

                #     if "error_list" in response:
                #         print("Error List : %s" % response['error_list'])

                # except CoolsmsException as e:
                #     print("Error Code : %s" % e.code)
                #     print("Error Message : %s" % e.msg)
