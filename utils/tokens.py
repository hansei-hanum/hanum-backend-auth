from env.environ import JWTEnv 
import jwt

from services.user import UserService

SECRET = JWTEnv.SECRET_KEY
ALGORITHM = JWTEnv.ALGORITHM

def check_auth(token):
    try:
        tmp = jwt.decode(token, SECRET, algorithms="HS256")
        return tmp
    except jwt.ExpiredSignatureError:
        return False, "Token Expired"
    except jwt.InvalidTokenError:
        return False, "Invalid Token"
    

def create_access_token(user: UserService):
    payload = {
        "sub": str(user.id),
        "name": user.name,
        "ver": user.verification,
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)