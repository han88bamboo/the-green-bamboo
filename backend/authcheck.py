# Port: 5030
# Routes: /authcheck (POST), /authcheckUser (POST), /authcheckProducer (POST), /authcheckVenue (POST)
# -----------------------------------------------------------------------------------------

import bson
import json
from bson import json_util
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

from bson.objectid import ObjectId


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
# [POST] Authenticates an account
# - Check if account exists in the "users", "producers", or "venues" collection. If so, check if the password matches.
# - Possible return codes: 200 (Authenticated), 400 (Account not found), 401 (Incorrect password), 500 (Error during authentication)
@app.route("/authcheck", methods= ['POST'])
def authcheck():

    try:
        loginInfo = request.get_json()


        # Check if user exists in the "users" collection
        userExistsRaw = db.users.find_one({"username": loginInfo["username"]})
        userExists = parse_json(userExistsRaw)
        if (userExists != None):

            # User exists, check if password matches
            if(str(userExists["hashedPassword"]) == str(loginInfo["password"])):
                return jsonify(
                    {   
                        "code": 200,
                        "id": userExists["_id"]["$oid"],
                        "role": "user",
                        "message": "Authenticated!"
                    }
                ), 200
            
            # Password does not match
            else:
                return jsonify(
                    {   
                        "code": 401,
                        "message": "Invalid username or password!"
                    }
                ), 401


        # Check if producer exists in the "producers" collection
        producerExistsRaw = db.producers.find_one({"producerName": loginInfo["username"]})
        producerExists = parse_json(producerExistsRaw)
        if (producerExists != None):

            # Producer exists, check if password matches
            if(str(producerExists["hashedPassword"]) == str(loginInfo["password"])):
                return jsonify(
                    {   
                        "code": 200,
                        "id": producerExists["_id"]["$oid"],
                        "role": "producer",
                        "message": "Authenticated!"
                    }
                ), 200
            
            # Password does not match
            else:
                return jsonify(
                    {   
                        "code": 401,
                        "message": "Invalid username or password!"
                    }
                ), 401


        # Check if venue exists in the "venues" collection
        venueExistsRaw = db.venues.find_one({"venueName": loginInfo["username"]})
        venueExists = parse_json(venueExistsRaw)
        if (venueExists != None):

            # Venue exists, check if password matches
            if(str(venueExists["hashedPassword"]) == str(loginInfo["password"])):
                return jsonify(
                    {   
                        "code": 200,
                        "id": venueExists["_id"]["$oid"],
                        "role": "venue",
                        "message": "Authenticated!"
                    }
                ), 200
            
            # Password does not match
            else:
                return jsonify(
                    {   
                        "code": 401,
                        "message": "Invalid username or password!"
                    }
                ), 401
        

        # Account does not exist
        return jsonify(
            {   
                "code": 400,
                "message": "An account of this username does not exist!"
            }
        ), 400


    # Error during authentication
    except Exception as e:
        return jsonify(
            {   
                "code": 500,
                "message": "An unknown error occurred while logging in, please try again."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Authenticates a user
# - Check if user exists in the "users" collection. If so, check if the password matches.
# - Possible return codes: 200 (Authenticated), 400 (User not found), 401 (Incorrect password), 500 (Error during authentication)
@app.route("/authcheckUser", methods= ['POST'])
def authcheckUser():

    try:
        # Check if user exists in the "users" collection
        loginInfo = request.get_json()
        userExistsRaw = db.users.find_one({"username": loginInfo["username"]})
        userExists = parse_json(userExistsRaw)

        # User does not exist
        if(userExists == None):
            return jsonify(
                {   
                    "code": 400,
                    "message": "An account of this type and username does not exist!"
                }
            ), 400
        
        # User exists, check if password matches
        if(str(userExists["hashedPassword"]) == str(loginInfo["password"])):
            return jsonify(
                {   
                    "code": 200,
                    "id": userExists["_id"]["$oid"],
                    "message": "Authenticated!"
                }
            ), 200
        
        # Password does not match
        else:
            return jsonify(
                {   
                    "code": 401,
                    "message": "Invalid username or password!"
                }
            ), 401
    
    # Error during authentication
    except Exception as e:
        return jsonify(
            {   
                "code": 500,
                "message": "An unknown error occurred while logging in, please try again."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Authenticates a producer
# - Check if producer exists in the "producers" collection. If so, check if the password matches.
# - Possible return codes: 200 (Authenticated), 400 (Producer not found), 401 (Incorrect password), 500 (Error during authentication)
@app.route("/authcheckProducer", methods= ['POST'])
def authcheckProducer():

    try:
        # Check if producer exists in the "producers" collection
        loginInfo = request.get_json()
        producerExistsRaw = db.producers.find_one({"producerName": loginInfo["username"]})
        producerExists = parse_json(producerExistsRaw)

        # Producer does not exist
        if(producerExists == None):
            return jsonify(
                {   
                    "code": 400,
                    "message": "An account of this type and username does not exist!"
                }
            ), 400
        
        # Producer exists, check if password matches
        if(str(producerExists["hashedPassword"]) == str(loginInfo["password"])):
            return jsonify(
                {   
                    "code": 200,
                    "id": producerExists["_id"]["$oid"],
                    "message": "Authenticated!"
                }
            ), 200
        
        # Password does not match
        else:
            return jsonify(
                {   
                    "code": 401,
                    "message": "Invalid username or password!"
                }
            ), 401
    
    # Error during authentication
    except Exception as e:
        return jsonify(
            {   
                "code": 500,
                "message": "An unknown error occurred while logging in, please try again."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Authenticates a venue
# - Check if venue exists in the "venues" collection. If so, check if the password matches.
# - Possible return codes: 200 (Authenticated), 400 (Venue not found), 401 (Incorrect password), 500 (Error during authentication)
@app.route("/authcheckVenue", methods= ['POST'])
def authcheckVenue():

    try:
        # Check if venue exists in the "venues" collection
        loginInfo = request.get_json()
        venueExistsRaw = db.venues.find_one({"venueName": loginInfo["username"]})
        venueExists = parse_json(venueExistsRaw)

        # Venue does not exist
        if(venueExists == None):
            return jsonify(
                {   
                    "code": 400,
                    "message": "An account of this type and username does not exist!"
                }
            ), 400
        
        # Venue exists, check if password matches
        if(str(venueExists["hashedPassword"]) == str(loginInfo["password"])):
            return jsonify(
                {   
                    "code": 200,
                    "id": venueExists["_id"]["$oid"],
                    "message": "Authenticated!"
                }
            ), 200
        
        # Password does not match
        else:
            return jsonify(
                {   
                    "code": 401,
                    "message": "Invalid username or password!"
                }
            ), 401
    
    # Error during authentication
    except Exception as e:
        return jsonify(
            {   
                "code": 500,
                "message": "An unknown error occurred while logging in, please try again."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Edit user password
# - Update user password with new password
# - Possible return codes: 201 (Updated), 401(Passwords do not match) , 404(User not exist), 500 (Error during update)
@app.route('/editPassword/<id>', methods=['POST'])
def editPassword(id):
    data = request.get_json()
    print(data)
    # if data contains image64
    if data["userType"] == "user":
        userRaw = db.users.find_one({"_id": ObjectId(id)})
    if data["userType"] == "producer":
        userRaw = db.producers.find_one({"_id": ObjectId(id)})
    if data["userType"] == "venue":
        userRaw = db.venues.find_one({"_id": ObjectId(id)})
        
    if userRaw is None:
        return jsonify(
            {   
                "code": 404,
                "data": {
                    "userID": id
                }
            }
        ), 404
    try: 
        if data['oldHash'] != userRaw['hashedPassword']:
            return jsonify(
                {   
                    "code": 401,
                    "data": {
                        "userID": id
                    }
                }
            ), 401
        else:
            if data["userType"] == "user":
                updatePassword = db.users.update_one({'_id': ObjectId(id)}, {'$set': {'hashedPassword': data['newHash']}})
            if data["userType"] == "producer":
                updatePassword = db.producers.update_one({'_id': ObjectId(id)}, {'$set': {'hashedPassword': data['newHash']}})
            if data["userType"] == "venue":
                updatePassword = db.venues.update_one({'_id': ObjectId(id)}, {'$set': {'hashedPassword': data['newHash']}})

            return jsonify(
                {   
                    "code": 201,
                    "data": {
                        "userID": id,
                    }
                }
            ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userID": id
                },
                "message": "An error occurred updating the password."
            }
        ), 500
# -----------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port = 5030)