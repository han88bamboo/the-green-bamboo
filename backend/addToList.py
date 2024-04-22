# Port: 5070
# Routes: /updateListing/<id> (PUT), /deleteListing/<id> (DELETE)
# Dataclass: listings
# -----------------------------------------------------------------------------------------

import bson
import json
from bson import json_util
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

from bson.objectid import ObjectId

import data
from datetime import datetime

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
# [PUT] adds a listing to have tried list 
# - Update "Drinks I Have Tried List" with specified id from the "listings" collection
# - Possible return codes: 200 (List Updated), 440 (Failed to add to list)
@app.route("/addToTried/", methods=['PUT'])
def addToTried():
    
    addedListing = request.get_json()
    date = datetime.strptime(addedListing["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    listingID = addedListing["listingID"]
    userID = ObjectId(addedListing["userID"])

   
    try:
        result = db.users.update_one(
            {"_id": userID},
            # {"$set": data.asdict(updatedBottle)}
            {"$push": {"drinkLists.Drinks I Have Tried.listItems": [
                date,
                listingID
            ]}})

        
        return jsonify(
            {
                "code": 200,
                "data": listingID,
                "message": "Listing was added into the list."
            }
        ), 200
    
    except Exception as e:
        
        return jsonify(
            {
                "code": 440,
                "data": listingID,
                "message": "Listing was not added into the list"
            }
        ), 440
    


# -----------------------------------------------------------------------------------------
# [PUT] adds a listing to have tried list 
# - Update "Drinks I Want To Try" List with specified id from the "listings" collection
# - Possible return codes: 210 (List Updated), 450 (Failed to add to list)
@app.route("/addToWant/", methods=['PUT'])
def addToWant():
    
    addedListing = request.get_json()
    date = datetime.strptime(addedListing["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    listingID = addedListing["listingID"]
    userID = ObjectId(addedListing["userID"])

   
    try:
        result = db.users.update_one(
            {"_id": userID},
            # {"$set": data.asdict(updatedBottle)}
            {"$push": {"drinkLists.Drinks I Want To Try.listItems": [
                date,
                listingID
            ]}})

        
        return jsonify(
            {
                "code": 210,
                "data": listingID,
                "message": "Listing was added into the list."
            }
        ), 210
    
    except Exception as e:
        
        return jsonify(
            {
                "code": 450,
                "data": listingID,
                "message": "Listing was not added into the list"
            }
        ), 450

# -----------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port = 5070)