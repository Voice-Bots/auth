from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.database import mongo, mongo_client, database
from src.schemas import BotId, Login, CreateAccount,CreateBot
from src.auth import current_user, check_access
from src.utils import (
    get_current_user_type, 
    unique_id, 
    get_current_datetime, 
    get_default_token_expire, 
    verify_password, 
    verify_token,
    login_req_url
)
from loguru import logger
import time

from src import utils, auth
app = FastAPI()



@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = mongo_client
    app.db = mongo
    app.users = app.mongodb_client['auth']['users']
    app.tokens = app.mongodb_client['auth']['tokens']
    
    

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    
    
@app.get("/handshake")
def handshake():
    return {
        "status": "ok"
    }
    

@app.middleware("http")
async def is_valid_token(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Headers = {request.headers}")
    authorization = request.headers.get("authorization","") or request.headers.get("Authorization","")
    access_token = authorization.split(" ")[-1]
    
    url = request.url
    if not login_req_url(url):
        logger.info(f"No autherization required = {url}")
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"URL = {url} :: process_time={process_time}")
        return response
    
    if verify_token(request,access_token):
        logger.info(f"autherization required = {url} .... checking token access")
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"URL = {url} :: process_time={process_time}")
        return response
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="invalid auth token")



@app.post("/login", status_code=200)
def login(request: Request, payload: Login):
    
    condition = payload.dict()
    condition.pop("password")
    result = request.app.db.get(collection=request.app.users, condition=condition)
    
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="invalid credentials")
    
    if not verify_password(
        plain_password=payload.password,
        hash_password=result.pop("password")
    ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    
    access_token = auth.generate_token(result)
    token_details = {
        "username":condition.get("username"),
        "access_token":access_token,
        "expires_at":get_default_token_expire(),
        "created_at":get_current_datetime()
    }
    result = request.app.db.put(collection=request.app.tokens, record=token_details)
    
    if "_id" in token_details:
        del token_details["_id"]
        
    logger.info(f"login DB result = {result} and returing = {token_details}")
    if result:
        return {"status":"success",**token_details}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    

@app.post("/createaccount", status_code=201)
def create_account(request: Request, payload: CreateAccount): #,crnt_user: dict=Depends(current_user)):
    
    record = payload.dict()
    create_account_type = record.pop("account_type")
    
    crnt_user = {}
    crnt_user.update({
        **record,
        "to_endpoint": create_account_type,
        "_type": "write"
    })
    created_by = crnt_user.get("username")
    retutn_data = {
        "account_type": create_account_type,
        "account_id": unique_id(),
        "created_at": get_current_datetime(),
        "created_by":created_by
    }
    if True: #check_access(crnt_user):
        record.update({
            "password": utils.hash(payload.password),
            **retutn_data
        })
        result = request.app.db.put(collection=request.app.users, record=record)
        logger.info(f"Account Creation DB result : {result}")
        if result:
            return {"status":"success",**retutn_data}
        raise  HTTPException(401, "Account Can not be created")    
    else:
        raise  HTTPException(401, "Account Can not be created")
    


@app.post("/createbot")
def createbot(request: Request,): #payload: CreateBot,crnt_user: dict=Depends(current_user)):
    
    # record = payload.dict()
    # crnt_user.update({
    #     **record,
    #     "to_endpoint": "createbot",
    #     "_type": "write"
    # })
    # if check_access(crnt_user):
        
    #     result = request.app.db.put(collection=request.app.users, record=record)
        
    if True:
        return True
    else:
        raise  HTTPException(401, "Access denied")


@app.post("/updatebotdetails")
async def updatebotdetails(request: Request, crnt_user: dict=Depends(current_user)):
    
    record = await request.json()
    logger.info(f"record : {record}")
    crnt_user.update({
        **record,
        "to_endpoint": "updatebotdetails",
        "_type": "write"
    })
    if check_access(crnt_user):
        
        result = request.app.db.put(collection=request.app.users, record=record)
        
        return True
    else:
        raise  HTTPException(401, "Access denied")



    
    
@app.post("/contacts", )
def contacts(payload: BotId, crnt_user: dict=Depends(current_user)):
    
    logger.info(f"payload : {payload}")
    logger.info(f"current_user : {crnt_user}")
    crnt_user.update({
        "to_endpoint": "contacts",
        "_type": "read"
    })
    if check_access(crnt_user):
        return True
    else:
        raise  HTTPException(401, "Access denied")
    
    

@app.post("/triggermany")
async def trigger_many(request: Request, crnt_user: dict=Depends(current_user)):
    
    record = await request.json()
    logger.info(f"record : {record}")
    crnt_user.update({
        **record,
        "to_endpoint": "triggermany",
        "_type": "write"
    })
    if check_access(crnt_user):
        
        result = request.app.db.put(collection=request.app.users, record=record)
        
        return True
    else:
        raise  HTTPException(401, "Access denied")

    