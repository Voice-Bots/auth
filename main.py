from fastapi import FastAPI, Request, HTTPException, status
from src.database import mongo, mongo_client
from src.schemas import Login, CreateBot
from loguru import logger

from src import utils, auth
app = FastAPI()



@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = mongo_client
    app.db = mongo
    app.users = app.mongodb_client['auth']['users']
    print("Added all configs")
    
    

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
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="You are not an user in our app")
    
    if not utils.verify_password(
        plain_password=payload.password,
        hash_password=result.pop("password")
    ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    
    access_token = auth.generate_token(result)
    
    return {
        "status": True,
        "access_token": access_token
    }
    