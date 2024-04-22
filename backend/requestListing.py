# Port: 5011
# Routes: /requestListing (POST), /requestListingModify/<requestID> (POST), /requestEdits (POST), /requestEditsModify/<requestID> (POST), /requestInaccuracy (POST), /requestReviewStatus/<requestID> (POST)
# Dataclass: RequestListings
# -----------------------------------------------------------------------------------------

import bson
import json
from bson import json_util
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

from bson.objectid import ObjectId
from datetime import datetime
import pytz

import data

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# app.config["MONGO_URI"] = "mongodb+srv://jwleong2020:uOfXCrxLPCjgyA92@greenbamboo.wbiambw.mongodb.net/GreenBamboo?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb+srv://jwleong2020:uOfXCrxLPCjgyA92@drinkx.eskadzx.mongodb.net/DrinkX?retryWrites=true&w=majority"
db = PyMongo(app).db

def parse_json(data):
    return json.loads(json_util.dumps(data))

# -----------------------------------------------------------------------------------------
# [POST] Request for listing creation
# - Insert entry into the "requestListings" collection. Follows requestListings dataclass requirements.
# - Duplicate listing check: If a listing with the same name exists, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@app.route("/requestListing", methods= ['POST'])
def requestListing():
    rawRequest = request.get_json()

    # Duplicate listing check: Reject if listing with the same bottle name already exists in the "listings" collection
    rawRequestName = rawRequest["listingName"]
    existingBottle = db.listings.find_one({"listingName": rawRequestName})
    if (existingBottle != None):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingName": rawRequestName
                },
                "message": "Bottle with the same name already exists."
            }
        ), 400
    
    # Insert new request into database
    newRequest = data.requestListings(**rawRequest)
    try:
        insertResult = db.requestListings.insert_one(data.asdict(newRequest))

        return jsonify(
            {
                "code": 201,
                "data": rawRequestName
            }
        ), 201
    
    except Exception as e:
        print(str(e))

        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingName": rawRequestName
                },
                "message": "An error occurred while submitting the request."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Edit submitted request for listing creation
# - Update entry with specified id from the "requestListings" collection. Follows requestListings dataclass requirements.
# - Duplicate listing check: If a listing with the same name exists, reject the request
# - Possible return codes: 201 (Updated), 400 (Duplicate Detected), 500 (Error during update)
@app.route("/requestListingModify/<string:requestID>", methods= ['POST'])
def requestListingModify(requestID):
    rawRequest = request.get_json()

    # Duplicate listing check: Reject if listing with the same bottle name already exists in the "listings" collection
    rawRequestName = rawRequest["listingName"]
    existingBottle = db.listings.find_one({"listingName": rawRequestName})
    if (existingBottle != None):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingName": rawRequestName
                },
                "message": "Bottle with the same name already exists."
            }
        ), 400
    
    # Update existing request in database
    updateRequest = data.requestListings(**rawRequest)
    try:
        updateResult = db.requestListings.update_one({"_id": ObjectId(requestID)}, {"$set": data.asdict(updateRequest)})

        return jsonify(
            {
                "code": 201,
                "data": rawRequestName
            }
        ), 201
    
    except Exception as e:
        print(str(e))

        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingName": rawRequestName
                },
                "message": "An error occurred while submitting the request."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Request for listing modification
# - Insert entry into the "requestEdits" collection. Follows requestEdits dataclass requirements.
# - Possible return codes: 201 (Created), 400 (Invalid Listing), 500 (Error during creation)
@app.route("/requestEdits", methods= ['POST'])
def requestEdits():
    rawRequest = request.get_json()

    # Check if edit request is linked to a listing that exists in the database
    rawListingID = rawRequest["listingID"]["$oid"]
    existingListing = db.listings.find_one({"_id": ObjectId(rawListingID)})

    if (existingListing == None):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingID": rawListingID
                },
                "message": "Linked listing is not valid!"
            }
        ), 400
    
    # Insert new edit request into database
    newRequest = data.requestEdits(**rawRequest)
    try:
        insertResult = db.requestEdits.insert_one(data.asdict(newRequest))

        return jsonify(
            {
                "code": 201,
                "data": rawListingID
            }
        ), 201
    
    except Exception as e:
        print(str(e))

        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingName": rawListingID
                },
                "message": "An error occurred while submitting the request."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Edit submitted request for listing modification
# - Update entry with specified id from the "requestEdits" collection. Follows requestEdits dataclass requirements.
# - Possible return codes: 201 (Updated), 400 (Invalid Listing), 500 (Error during update)
@app.route("/requestEditsModify/<string:requestID>", methods= ['POST'])
def requestEditsModify(requestID):
    rawRequest = request.get_json()

    # Check if edit request is linked to a listing that exists in the database
    rawListingID = rawRequest["listingID"]["$oid"]
    existingListing = db.listings.find_one({"_id": ObjectId(rawListingID)})

    if (existingListing == None):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingID": rawListingID
                },
                "message": "Linked listing is not valid!"
            }
        ), 400

    # Update existing request in database
    updateRequest = data.requestEdits(**rawRequest)
    try:
        updateResult = db.requestEdits.update_one({"_id": ObjectId(requestID)}, {"$set": data.asdict(updateRequest)})

        return jsonify(
            {
                "code": 201,
                "data": rawListingID
            }
        ), 201
    
    except Exception as e:
        print(str(e))

        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingName": rawListingID
                },
                "message": "An error occurred while submitting the request."
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
# [POST] Request for listing modification in venue menu
# - Insert entry into the "requestInaccurate" collection. Follows requestInaccuracy dataclass requirements.
# - Possible return codes: 201 (Created), 400 (Duplicate request), 500 (Error during creation)
@app.route("/requestInaccuracy", methods= ['POST'])
def requestInaccuracy():
    rawRequest = request.get_json()

    # Check if inaccuracy request is already submitted for the same bottle for a venue in the database
    rawListingID = rawRequest["listingID"]["$oid"]
    rawVenueID = rawRequest["venueID"]
    rawUserID = rawRequest["userID"]
    existingListing = db.requestInaccuracy.find_one({"listingID": ObjectId(rawListingID), "venueID":ObjectId(rawVenueID), "userID":ObjectId(rawUserID)})

    if (existingListing != None):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingID": rawListingID
                },
                "message": "Duplicate request for inaccuracy!"
            }
        ), 400
    
    # Insert new edit request into database
    rawRequest["venueID"] = ObjectId(rawVenueID)
    rawRequest["userID"] = ObjectId(rawUserID)
    rawRequest["listingID"] = ObjectId(rawListingID)
    rawRequest["reviewStatus"] = False
    rawRequest["reportDate"] = datetime.now(pytz.timezone('Etc/GMT-8'))
    newRequest = data.requestInaccuracy(**rawRequest)

    try:
        insertResult = db.requestInaccuracy.insert_one(data.asdict(newRequest))

        return jsonify(
            {
                "code": 201,
                "data": rawListingID
            }
        ), 201
    
    except Exception as e:
        print(str(e))

        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingName": rawListingID
                },
                "message": "An error occurred while submitting the request."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Edit review status of a submitted request
# - Update entry with specified id from the specified collection.
# - Possible return codes: 201 (Updated), 500 (Error during update)

@app.route("/requestReviewStatus/<string:requestID>", methods= ['POST'])
def requestReviewStatus(requestID):

    requestIDObject = ObjectId(requestID)
    updateRequest = request.get_json()
    targetCollection = updateRequest["targetCollection"]
    status = updateRequest["reviewStatus"]

    try:
        updateResult = db[targetCollection].update_one({"_id": requestIDObject}, {"$set": {"reviewStatus": status}})

        return jsonify(
            {
                "code": 201,
                "data": requestID
            }
        ), 201
    
    except Exception as e:
        print(str(e))

        return jsonify(
            {
                "code": 500,
                "data": {
                    "requestID": requestID
                },
                "message": "An error occurred while updating the review status."
            }
        ), 500

# -----------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port = 5011)