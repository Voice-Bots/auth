
from pydantic import BaseModel, EmailStr, validator
from typing import List
from src.user_types import (ACCOUNT_TYPES,
                            ADMIN_TYPE,
                            MANAGER_TYPE,
                            DEVELOPER_TYPE,
                            TESTER_TYPE,
                            CADMIN_TYPE,
                            CUSER_TYPE)

from datetime import datetime
import re
from src.user_types import access_types_obj

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
    # access_types: List
    
    
    @validator("account_type")
    def check_existing_categories(cls, value):
        
        all_types = ACCOUNT_TYPES.keys()
        
        print(f"Checking existing categories, we got value as {value} | {all_types}")
        condition = value in all_types
        print(f"condition: {condition}")
        if ACCOUNT_TYPES.get(value):
            return value
        
        raise ValueError(f"Account type must be one of {(all_types)}")


    @validator("username")
    def validate_username(cls, username):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if(re.fullmatch(email_regex, username)):
            return username
        raise ValueError(f"username should be in email format")
    

    # @validator("access_types")
    # def validate_access_types(cls, access_types:[]):
        
    #     if access_types:
    #         if isinstance(access_types, str):
    #             access_types = [access_types]
            
    #         if access_types in access_types_obj.access_types:
    #             return access_types
    #     raise ValueError(f"Access types should be write, read, update or delete")
        
        


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
    

class DemoRegistration(BaseModel):
    phone_number: int

    @validator("phone_number")
    def check_existing_categories(cls, phone_number):
        
        phone_number = str(phone_number).replace("+", "").replace(" ", "")
        if phone_number.startswith("91") and len(phone_number) >=12:
            phone_number = phone_number.replace("91", "")

        phone_number = int(phone_number)
        if len(str(phone_number)) == 10:
            return phone_number
    
        raise ValueError(f"Phone number is invalid")
    