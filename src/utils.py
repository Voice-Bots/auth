from passlib.context import CryptContext
from src.user_types import ACCOUNT_TYPES
from loguru import logger

import uuid

password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash(password):
    return password_context.hash(password)


def verify(plain_password, hash_password):
    matched = password_context.verify(plain_password, hash_password)
    logger.info(f"password matched : {matched}")
    return matched

def get_current_user_type(payload):
    logger.info(f"got payload: {payload}")
    user_type = payload.get("account_type")
    
    return ACCOUNT_TYPES.get(user_type)

def unique_id(text=""):
    return str(uuid.uuid4().hex)
    
    