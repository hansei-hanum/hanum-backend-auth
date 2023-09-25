from google.oauth2._service_account_async import Credentials
from google.auth.transport._aiohttp_requests import Request

SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]

credentials = Credentials.from_service_account_file("firebase-cred.json", scopes=SCOPES)


async def get_access_token():
    if credentials.valid is False:
        request = Request()
        await credentials.refresh(request)

    return credentials.token
