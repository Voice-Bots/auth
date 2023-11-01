import jwt
import uuid
from sanic import Blueprint, Sanic, response
from database import mongo

app = Sanic(__name__)


app.config.SECRET = "3a03ecd3660d419ba90599e7f02daaff"




@app.get("/handshake")
async def handshake(request):
    return {
        "status": "ok"
    }

@app.post("/check-login")
async def login_required(request):
    # if the token is already in session
    request_json = request.json
    token = request_json.get("token")
    email = request_json.get("email")
    if token and email:
        db_result = mongo.check_token_exists(email, token)
        
        if db_result:
            return response.json({
                "logged_in":True,
                "token":token, 
                "email":email
            }, status=200)
        
    return response.json({
        "logged_in":False,
        "token":None
    }, status=200)
    


@app.post("/login")
async def login(request):

    # these details user will provide
    request_json = request.json
    email = request_json['email']
    user_pwd = request_json['pwd']

    user_credentials = {
        "email":email,
        "password":user_pwd,
    }

    # get db details
    db_details = mongo.check_user_exists(email=email)
    if not db_details: # need to sign up , account is not in our db
        return response.json({
            "next_action":{
                "url":"/signup",
            },
            "status":"failed",
            "message":"email is not in our records, please signup"
        }, status=403)
    
    
    db_pwd = db_details['password']
    salt = db_details['salt']
    user_credentials["salt"] = salt

    enc_pwd = jwt.encode(user_credentials, request.app.config.SECRET, algorithm="HS256")

    if db_pwd == enc_pwd:
     
        token = jwt.encode({"uuid":uuid.uuid4().hex}, request.app.config.SECRET, algorithm="HS256")

        # update the token in db
        record = {"$set":{
            "token":token
        }}
        is_updated = mongo.update_credentials(email, record)
        
        
        
        return response.json({
            "token":token,
            "status":"success",
            "message":"token has fetched successfully"
        }, status = 200)

    else:
        return response.json({
            "status":"failed",
            "message":"password is wrong"
        }, status = 401)

@app.post("/signup")
async def signup(request):

    request_json = request.json

    # these details user will provide
    email = request_json['email']
    pwd = request_json['pwd']
    cnfm_pwd = request_json['cnfm_pwd']

    # check the email is already existing in db
    is_user_exists = mongo.check_user_exists(email=email)
    if is_user_exists:
        return response.json({
            "next_action":{
                "url":"/login",
            },
            "status":"failed",
            "message":"email is already exiting in our database"
        },status = 403)
    

    # check password and confirm password are equal
    if pwd == cnfm_pwd:
        salt = uuid.uuid4().hex
        user_credentials = {
            "email":email,
            "password":pwd,
            "salt":salt
        }
        password = jwt.encode(user_credentials, request.app.config.SECRET, algorithm="HS256")

        token = jwt.encode({"uuid":uuid.uuid4().hex}, request.app.config.SECRET, algorithm="HS256")
        
        # store below details
        credentials = {
            "email":email,
            "password":password,
            "salt":salt,
            "token":token
        }

        is_saved = mongo.save_user_credentials(credentials=credentials)

        return response.json({
            "token":token,
            "status":"success",
            "message":"successfully account got created"
        }, status = 200)

    else:
        return response.json({
            "status":"failed",
            "message":"both passwords are not matching"
        }, status=401)
        
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5858, debug=True)
    