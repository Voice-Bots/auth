from fastapi import Request, HTTPException,  Depends, APIRouter
from src.schemas import CreateAccount,CreateBot
from src.auth import current_user, check_access, check_existing_username
from src.utils import unique_id,  hash
from loguru import logger

users_router = APIRouter()


@users_router.get("user/list")
async def list_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@users_router.post("user/create")
def create_user(request: Request, payload: CreateAccount,crnt_user: dict=Depends(current_user)):
    
    record = payload.dict()
    create_account_type = record.pop("account_type")
    
    crnt_user.update({
        **record,
        "to_endpoint": create_account_type,
        "_type": "write"
    })

    user_status, user_msg = check_existing_username(crnt_user,request)
    if not user_status:
        return user_msg
    
    if check_access(crnt_user):
        record.update({
            "password": hash(payload.password),
            "account_type": create_account_type,
            "account_id": unique_id(),
            "to_endpoint": create_account_type,
            "_type": "write",
            "inactive":False
        })
        
        result = request.app.db.put(collection=request.app.users, record=record)
        
        return True
    else:
        raise  HTTPException(401, "Access denied")
    


@users_router.get("user/update")
async def update_user():
    return [{"username": "Rick"}, {"username": "Morty"}]

@users_router.post("user/delete")
def delete_user(request: Request, crnt_user: dict=Depends(current_user)):
    
    if check_access(crnt_user):
        account_id : crnt_user.get("account_id")
        _filter = {
            "account_id":account_id,
            "inactive":True
        }
        result = request.app.db.put(collection=request.app.users, record=_filter)
        
        return True
    else:
        raise  HTTPException(401, "Access denied")
