import os
from pymongo import MongoClient

# mongo client
if os.environ.get("ENV") == "prod":
    # in future we will add db URL
    pass
else:
    mongo_url = "mongodb://172.17.0.2:27017/"
    # mongo_url = "mongodb://localhost:27017/"

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

    def get(self, collection, condition=None, project=None):
        if condition is None:
            condition = {}
        if project is None:
            project = {"_id": 0}
        
        print(f"condition: {condition} project: {project}")
        try:
            db_result = collection.find_one(filter=condition, projection=project)
            print(f"db_result:{db_result}")
            if db_result:
                return db_result
            else:
                return {}
        except Exception as err:
            print(f"exception {err} ")
    
    def put(self, collection,  record):
        db_result = collection.insert_one(record)
        if db_result:
            return True
        else:
            return False        

    def update(self, collection, condition, record):
        
        db_result = collection.update_one(filter=condition, update=record)
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

if __name__ == '__main__':
    mongo.get(collection=mongo_client['auth']['users'], condition={"username":"hemanth@gmail.com","password":"hemanth"})
    