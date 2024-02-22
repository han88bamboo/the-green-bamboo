# Port: 5202
# Routes: /createAccount (POST)
# -----------------------------------------------------------------------------------------

import bson
import json
from bson import json_util
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from werkzeug.local import LocalProxy

from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId

import data

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config["MONGO_URI"] = "mongodb+srv://jwleong2020:uOfXCrxLPCjgyA92@greenbamboo.wbiambw.mongodb.net/GreenBamboo?retryWrites=true&w=majority"
db = PyMongo(app).db

def parse_json(data):
    return json.loads(json_util.dumps(data))

# -----------------------------------------------------------------------------------------
# [POST] Creates an Account
# - Insert entry into the "users" collection. Follows reviews dataclass requirements.
# - Duplicate review check: If a user with the same username, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@app.route("/createAccount", methods= ['POST'])
def createAccount():
    rawAccount = request.get_json()
    rawUsername= rawAccount['username']
    # Duplicate listing check: Reject if review with the same userID and reviewTarget exists in the database
    existingAccount = db.users.find_one({"username": rawUsername})
    if(existingAccount!= None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "userName": rawUsername
                },
                "message": "Username already exists."
            }
        ), 400
    
    
    # Insert new review into database
    newAccount = data.users(**rawAccount)
    try:
        insertResult = db.users.insert_one(data.asdict(newAccount))

        return jsonify( 
            {   
                "code": 201,
                "data": rawUsername
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userame": rawUsername
                },
                "message": "An error occurred creating the account."
            }
        ), 500

# -----------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port = 5202)