
from pydantic import BaseModel, EmailStr, validator
from src.user_types import (ACCOUNT_TYPES,
                            ADMIN_TYPE,
                            MANAGER_TYPE,
                            DEVELOPER_TYPE,
                            TESTER_TYPE,
                            CADMIN_TYPE,
                            CUSER_TYPE)

from datetime import datetime

USERNAME_TYPE = EmailStr



class BotId(BaseModel):
    bot_id: str


class Login(BaseModel):
    username: USERNAME_TYPE
    password: str


class CreateAccount(BaseModel):
    username: USERNAME_TYPE
    password: str
    account_type: str
    
    
    @validator("account_type")
    def check_existing_categories(cls, value):
        # all_types = [ADMIN_TYPE,
        #             MANAGER_TYPE,
        #             DEVELOPER_TYPE,
        #             TESTER_TYPE,
        #             CADMIN_TYPE,
        #             CUSER_TYPE]
        
        all_types = ACCOUNT_TYPES.keys()
        
        print(f"Checking existing categories, we got value as {value} | {all_types}")
        condition = value in all_types
        print(f"condition: {condition}")
        if ACCOUNT_TYPES.get(value):
            return value
        
        raise ValueError(f"Account type must be one of {(all_types)}")
    
class CreateBot(BaseModel):
    bot_id: str
    client_name: str
    bot_type: str
    
    
    @validator("bot_type")
    def check_existing_categories(cls, value):
        print(f"Checking bot_type")
        all_types = [
            "kpi",
            "speech",
            "hybrid"
        ]
        
        print(f"Checking existing categories, we got value as {value} | {all_types}")
        condition = value in all_types
        print(f"condition: {condition}")
        if condition:
            return value
        
        raise ValueError(f"Bot type must be one of {(all_types)}")
    
    
class Token(BaseModel):
    access_token : str
    token_type : str
    
class TokenData(BaseModel):
    username: USERNAME_TYPE
    password: str
    account_type: str
    