# Authentication and Authrization

UI SignUp and SingOut
======================
    SingUp
        1. Microsoft
        2. Google

        * Very first user should enter phone number (In phase-2, here we will verify with mail and phone number by sending OTP)

        * If user is not referral which means, user is direct connection so he can get admin access 

        * API Key should be created once user gets created.
        
    Login 

        * Automatic login check with 3rd party 

API Autherization
==================

1. ../get-token
    
    * user should send API key to get token
        - Internal if token is already present in redis, we will increase the expiry time
            Ex: existing token has only 30 min left, we will reset token expiry to 60 min 

            "api_key":{
                "token":"",
            }
    
    * Request
        curl --location 'http://0.0.0.0:8000/get-token' \
            --header 'Content-Type: application/json' \
            --data '{
                "api_key":"a6b2d038-4eb1-4ca1-a3b4-2cf783ad55e1"
            }'
        

    * Response

        - Token should have the data of scopes (UNIQUEY KEY + API KEY + SCOPES = Auth Token) 
        - All three data we should store in db for future purpose

        Sucesss
        =======
        {
            "data":{
                "auth_token":"",
            }
            "status":"sucess",
            "code":200,
            "message":"token sucessfully created"
        }

        Failure
        =======
        {
            "data":{}
            "status":"failed",
            "code":411,
            "message":"reason"
        }


2. ../<Any API>

    * Request
        curl --location 'http://0.0.0.0:8000/any-api' \
            --header 'x-authorization: Agent eiwjfjjiowenfEWIF' \
            --header 'x-api-key: JHBJB' // optional

    * API Validation

        1. Token exist in redis or not
        2. Scope of API

    
    * Response  

        If all validations are pass, Return respnose regarding api

        If any one validations fail
            {
                "data":[]
                "status":"failed",
                "code":422,
                "message":"reason message"
            }



From UI Perspctive

    * Where ever user goes in website api key exipry should increase automatically




Limitations & Problems
=========================
1. when user scopes updated, how do we handle in the redis, because redis auth token will have the scopes
    - From Website Perspective

    - From API user Perspective

2. when user created new api key by deleting existing current, how do we handle in redis
    - From Website Perspective

    - From API user Perspective

3. 
