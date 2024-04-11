import base64
import hashlib
import hmac
import aiohttp
from datetime import datetime, timezone
import random
import string
from urllib.parse import urlparse
from env import SENSEnv  

class SMSSender:
    def __init__(self):
        self.access_key = SENSEnv.ACCESS_KEY
        self.secret_key = SENSEnv.SECRET_KEY
        self.phone_number = SENSEnv.PHONE_NUMBER

    def generate_salt(self, length=64):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def signature(self, method: str, url_path: str):
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        salt = self.generate_salt()
        message = f"{timestamp}{salt}"

        
        signature = hmac.new(
            self.secret_key.encode("utf-8"),  
            message.encode("utf-8"),          
            hashlib.sha256                    
        ).hexdigest()  

        return {
            "timestamp": timestamp,
            "salt": salt,
            "signature": signature
        }

    async def sendMessage(self, to: str, message: str):
        url = f"https://api.coolsms.co.kr/messages/v4/send-many/detail"
        sign_data = self.signature("POST", urlparse(url).path)

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"HMAC-SHA256 apiKey={self.access_key}, date={sign_data['timestamp']}, salt={sign_data['salt']}, signature={sign_data['signature']}"
        }

        json_body = {
            "messages":[
                {
                    "type": "SMS",
                    "from": self.phone_number,
                    "text": message,
                    "to": to
                }
            ]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=json_body) as response:
                response.raise_for_status()
                return await response.json()
            
