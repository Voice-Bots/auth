from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.database import mongo, mongo_client, database
from src.schemas import BotId, Login, CreateAccount,CreateBot
from src.auth import current_user, check_access
from src.utils import get_current_user_type, unique_id
from loguru import logger

from src import utils, auth
app = FastAPI()



@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = mongo_client
    app.db = mongo
    app.users = app.mongodb_client['auth']['users']
    
    

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    
    
@app.get("/handshake")
def handshake():
    return {
        "status": "ok"
    }
    

@app.post("/login")
def login(request: Request, payload: Login):
    
    condition = payload.dict()
    condition.pop("password")
    result = request.app.db.get(collection=request.app.users, condition=condition)
    
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="invalid credentials")
    
    if not utils.verify(
        plain_password=payload.password,
        hash_password=result.pop("password")
    ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    
    access_token = auth.generate_token(result)
    
    return {
        "status": True,
        "access_token": access_token
    }
    

@app.post("/createaccount")
def create_account(request: Request, payload: CreateAccount,crnt_user: dict=Depends(current_user)):
    
    record = payload.dict()
    create_account_type = record.pop("account_type")
    
    crnt_user.update({
        **record,
        "to_endpoint": create_account_type,
        "_type": "write"
    })
    if check_access(crnt_user):
        record.update({
            "password": utils.hash(payload.password),
            "account_type": create_account_type,
            "account_id": unique_id()
        })
        
        result = request.app.db.put(collection=request.app.users, record=record)
        
        return True
    else:
        raise  HTTPException(401, "Access denied")
    


@app.post("/createbot")
def createbot(request: Request, payload: CreateBot,crnt_user: dict=Depends(current_user)):
    
    record = payload.dict()
    crnt_user.update({
        **record,
        "to_endpoint": "createbot",
        "_type": "write"
    })
    if check_access(crnt_user):
        
        result = request.app.db.put(collection=request.app.users, record=record)
        
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

    