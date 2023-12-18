from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from src.utils import get_current_user_type
from loguru import logger
import os

oauth_schema = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = os.environ.get("secret_key") or "B5418CF9F2C94A16A42A546FFA6C2FE9"
ALGORITHM = os.environ.get("password_algo") or "HS256"
TOKEN_EXPIRATION = os.environ.get("token_expiration") or 60 # minutes

def generate_token(payload: dict, ):
    expire_in = datetime.now() + timedelta(minutes=TOKEN_EXPIRATION)
    payload["exp"] = expire_in
    if "username" in payload:
        del payload['username']
    logger.info(f"generating token for {payload}")
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    

def extract_payload(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    except JWTError:
        raise credentials_exception
    except Exception as err:
        logger.info(f"exception while retrieving token : {err}")
    else:
        logger.info(f"retrived payload from token: {payload}")
        return payload


def current_user(token:str=Depends(oauth_schema)):
    logger.info(f"getting current user : {token}")
    credentials_exception = HTTPException(status_code=401, detail="could not validate credentials")
    return extract_payload(token, credentials_exception)

def check_access(payload):
    credentials_exception = HTTPException(status_code=401, detail="Not authorized to access")
    logger.info(f"payload : {payload}")
    current_user_type = get_current_user_type(payload)
    logger.info(f"current_user_type : {current_user_type}")
    to = payload.get("to_endpoint")
    _type = payload.get("_type")
    logger.info(f"_to : {to} _type : {_type}")

    
    access = current_user_type().has_access(to, _type)
    
    logger.info(f"{_type} access to {to} : {access}")
    return access
    
def check_existing_username(payload, request):
    
    try:
        username = payload['username']
    except:
        return False, "username key should pass in payload"
    else:
        condition = {
            "username":username
        }
        result = request.app.db.get(collection=request.app.users, condition=condition)
        if result:
            return False, "User is already existing in our records"
        return True, ""