from Env.environ import JwtEnv 
import jwt

from database.DTO.Response import JwtPayloadResponse

SECRET = JwtEnv.SECRET_KEY
ALGORITHM = "HS256"

def check_auth(token):
    try:
        tmp = jwt.decode(token, SECRET, algorithms="HS256")
        return tmp
    except jwt.ExpiredSignatureError:
        return False, "Token Expired"
    except jwt.InvalidTokenError:
        return False, "Invalid Token"
    

def create_access_token(user: JwtPayloadResponse):
    payload = {
        "sub": str(user.id),
        "name": user.name,
        "ver": user.verification,
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)