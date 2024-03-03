from google.oauth2._service_account_async import Credentials
from google.auth.transport._aiohttp_requests import Request
from aiohttp import ClientSession

SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]

credentials = Credentials.from_service_account_file("firebase-cred.json", scopes=SCOPES)


async def get_access_token():
    if credentials.valid is False:
        async with ClientSession(auto_decompress=False) as session:
            request = Request(session=session)
            await credentials.refresh(request)

    return credentials.token
