import os
from pymongo import MongoClient

# mongo client
mongo_url = os.environ.get('mongo_url')
mongo_client = MongoClient(mongo_url)

# database
database = "auth"
db = mongo_client[database]

# collections
login = "login"
tokens = "tokens"

login_col = db[login]
tokens_col = db[tokens]



class MongoDB():

    def check_user_exists(self, email):

        db_result = login_col.find_one(filter={"email":email})
        print(db_result)
        if db_result:
            return db_result
        else:
            return {}
    
    def save_user_credentials(self, credentials):

        # checking basic validation of email
        email = credentials.get("email")
        if not email:
            return False
        
        db_result = login_col.insert_one(credentials)
        if db_result:
            return True
        else:
            return False        


    def update_credentials(self, email, record):
        
        if not email:
            return False
        
        db_result = login_col.update_one(filter={"email":email}, update=record)
        if db_result:
            return True
        else:
            return False  

        
    def check_token_exists(self, email, token):
        
        filter = {
            "email":email,
            "token":token
        }

        db_result = login_col.find_one(filter)
        if db_result:
            return True
        else:
            return False




mongo = MongoDB()