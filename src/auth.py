from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from src.utils import get_current_user_type
from loguru import logger

oauth_schema = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "random secret key"
ALGORITHM = "HS256"
TOKEN_EXPIRATION = 30

def generate_token(payload: dict, ):
    expire_in = datetime.now() + timedelta(minutes=TOKEN_EXPIRATION)
    payload["exp"] = expire_in
    logger.info(f"generating token for {payload}")
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    

def verify_token(token: str, credentials_exception):
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
    credentials_exception = HTTPException(status_code=401, detail="could not validate credentials")
    return verify_token(token, credentials_exception)

def check_access(payload):
    credentials_exception = HTTPException(status_code=401, detail="not authorized to access")
    logger.info(f"payload : {payload}")
    current_user_type = get_current_user_type(payload)
    logger.info(f"current_user_type : {current_user_type}")
    to = payload.get("to_endpoint")
    _type = payload.get("_type")
    return current_user_type().has_access(to, _type)
    