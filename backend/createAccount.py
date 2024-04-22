# Port: 5031
# Routes: /createAccount (POST)
# -----------------------------------------------------------------------------------------

import bson
import json
from bson import json_util
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

from bson.objectid import ObjectId

from datetime import datetime

import data

from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)  # Allow all requests

load_dotenv()
app.config["MONGO_URI"] = os.getenv('MONGO_DB_URL')
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
    rawAccount['joinDate'] = datetime.strptime(rawAccount['joinDate'], "%Y-%m-%dT%H:%M:%S.%fZ")# convert date to datetime object
    rawAccount['birthday'] = datetime.strptime(rawAccount['birthday'], "%Y-%m-%d")# convert birthday to datetime object
    # rawAccount['birthday'] = datetime.strftime(rawAccount['birthday'], "%Y-%m-%dT%H:%M:%S.%fZ")# format birthday to desired object type
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
# -----------------------------------------------------------------------------------------
# [POST] Creates a Business Account Request
# - Insert entry into the "accountRequests" collection. Follows reviews dataclass requirements.
# - Duplicate review check: If a user with the same username, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@app.route("/createAccountRequest", methods= ['POST'])
def createAccountRequest():
    rawAccount = request.get_json()
    rawEmail= rawAccount['email']
    rawAccount['joinDate'] = datetime.strptime(rawAccount['joinDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
    # Duplicate listing check: Reject if review with the same userID and reviewTarget exists in the database
    existingAccount = db.accountRequests.find_one({"email": rawEmail})
    if(existingAccount!= None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "userName": rawEmail
                },
                "message": "Request already exists."
            }
        ), 400
    
    
    # Insert new review into database
    # newAccount = data.users(**rawAccount)
    try:
        insertResult = db.accountRequests.insert_one(rawAccount)

        return jsonify( 
            {   
                "code": 201,
                "data": rawEmail
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "email": rawEmail
                },
                "message": "An error occurred creating the account request."
            }
        ), 500
# -----------------------------------------------------------------------------------------
# [POST] Updates a Business Account Request
@app.route("/updateAccountRequest", methods= ['POST'])
def updateAccountRequest():
    data = request.get_json()
    print(data)
    requestID = data['requestID']
    reviewStatus = data['reviewStatus']

    try: 
        updateReviewStatus = db.accountRequests.update_one({'_id': ObjectId(requestID)}, {'$set': {'reviewStatus': reviewStatus}})

        return jsonify(
            {   
                "code": 201,
                "data": {
                    "requestID": requestID,
                    "reviewStatus": reviewStatus
                }
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "data": {
                        "requestID": requestID,
                        "reviewStatus": reviewStatus
                    }
                },
                "message": "An error occurred updating the mod request."
            }
        ), 500
# -----------------------------------------------------------------------------------------
# [POST] Creates an Account
# - Insert entry into the "producers" collection. 
@app.route("/createProducerAccount", methods= ['POST'])
def createProducerAccount():
    data = request.get_json()
    print(data)
    newBusinessData = data["newBusinessData"]

    print(newBusinessData["producerName"])

    existingAccount = db.producers.find_one({"producerName": newBusinessData['producerName']})
    if(existingAccount!= None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "producerName": newBusinessData['producerName']
                },
                "message": "Producer Name already exists."
            }
        ), 400

    try:
        insertResult = db.producers.insert_one(newBusinessData)
        newBusinessData['_id'] = str(newBusinessData['_id'])

        return jsonify( 
            {   
                "code": 201,
                "data": newBusinessData
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userame": newBusinessData
                },
                "message": "An error occurred creating the account."
            }
        ), 500
# -----------------------------------------------------------------------------------------
# [POST] Creates a Venue Account
# - Insert entry into the "venues" collection.
@app.route("/createVenueAccount", methods= ['POST'])
def createVenueAccount():
    data = request.get_json()
    print(data)
    newBusinessData = data["newBusinessData"]

    print(newBusinessData["venueName"])

    existingAccount = db.venues.find_one({"venueName": newBusinessData['venueName']})
    if(existingAccount!= None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "venueName": newBusinessData['venueName']
                },
                "message": "Venue Name already exists."
            }
        ), 400

    try:
        insertResult = db.venues.insert_one(newBusinessData)
        newBusinessData['_id'] = str(newBusinessData['_id'])

        return jsonify( 
            {   
                "code": 201,
                "data": newBusinessData
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userame": newBusinessData
                },
                "message": "An error occurred creating the account."
            }
        ), 500

# -----------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port = 5031)