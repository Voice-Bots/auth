from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from src.user_types import ACCOUNT_TYPES
from loguru import logger
from pytz import timezone
import uuid
from datetime import datetime, timedelta
import os

password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# when deploying project we can give whichever zone we want, and depends on that timezone, datetime will be stored in db
zone = os.environ.get('TIMEZONE') or "Asia/Kolkata"
logger.info(f"ZONE = {zone}")
TIMEZONE = timezone(zone)
TOKEN_EXPIRATION = 60 # minutes

def hash(password):
    return password_context.hash(password)


def verify_password(plain_password, hash_password):
    matched = password_context.verify(plain_password, hash_password)
    logger.info(f"password matched : {matched}")
    return matched

def verify_token(request,access_token):
    condition = {
        "access_token":access_token
    }
    if access_token:
        result = request.app.db.get(collection=request.app.tokens, condition=condition)
        logger.info(f"verify token DB result = {result}")
        if result:
            return True            
    return False        

def get_current_user_type(payload):
    logger.info(f"got payload: {payload}")
    user_type = payload.get("account_type")
    
    return ACCOUNT_TYPES.get(user_type)

def unique_id(text=""):
    return str(uuid.uuid4().hex)
    
def get_current_datetime():
    now = datetime.now()
    now = now.astimezone(TIMEZONE)
    print(now)
    return f"ISODate('{now.isoformat()}')"

def get_default_token_expire():
    expires_at = datetime.now() + timedelta(minutes=TOKEN_EXPIRATION)
    expires_at = expires_at.astimezone(TIMEZONE)
    return f"ISODate('{expires_at.isoformat()}')"


def return_failed_response(**kwargs):
    logger.info(f"kwargs={kwargs}")
    if kwargs.get("status_code"):
        return JSONResponse(content=kwargs, status_code=kwargs.get("status_code"))
    return JSONResponse(content=kwargs, status_code=400)
    