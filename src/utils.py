from passlib.context import CryptContext
from src.user_types import ACCOUNT_TYPES
from loguru import logger
from pytz import timezone
import uuid
from datetime import datetime, timedelta
import os
from src.login_req_urls import LOGIN_REQUIRED_URLS

password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# when deploying project we can give whichever zone we want, and depends on that timezone, datetime will be stored in db
zone = os.environ.get('TIMEZONE') or "Asia/Kolkata"
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
    now = datetime.now(TIMEZONE)
    return f"ISODate({now.isoformat()})"

def get_default_token_expire():
    expires_at = datetime.now(TIMEZONE) + timedelta(minutes=TOKEN_EXPIRATION)
    return f"ISODate({expires_at.isoformat()})"

def login_req_url(url):
    logger.info(f"URL = {url}")
    api = "/"+"/".join(str(url).split("/")[3:])
    logger.info(f"API = {api}")
    if api in LOGIN_REQUIRED_URLS:
        return True
    return False