# Port: 5021
# Routes: /createReview (POST)
# Dataclass: reviews
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
# [POST] Creates a review
# - Insert entry into the "reviews" collection. Follows reviews dataclass requirements.
# - Duplicate review check: If a review with the same userID and reviewTarget exists, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@app.route("/createReview", methods= ['POST'])
def createReviews():
    rawReview = request.get_json()
    rawReview['reviewTarget'] = ObjectId(rawReview['reviewTarget'])  # Convert reviewTarget to ObjectId
    rawReview['userID'] = ObjectId(rawReview['userID'])  # Convert userID to ObjectId
    rawReview['createdDate'] = datetime.strptime(rawReview['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ")# convert date to datetime object

    if len(rawReview['taggedUsers']) >0:
        temp_tag_id =[]
        for id in rawReview['taggedUsers']:
            temp_tag_id.append(ObjectId(id))
        rawReview['taggedUsers'] = temp_tag_id
    if len(rawReview['flavorTag']) >0:
        temp_flavour_tag =[]
        for id in rawReview['flavorTag']:
            temp_flavour_tag.append(ObjectId(id['$oid']))
        rawReview['flavorTag'] = temp_flavour_tag

    # Duplicate listing check: Reject if review with the same userID and reviewTarget exists in the database
    rawReviewBottle = rawReview["reviewTarget"]
    rawReviewUserID = rawReview["userID"]
    existingReview = db.reviews.find_one({"reviewTarget": rawReviewBottle, "userID": rawReviewUserID})
    if(existingReview != None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "listingName": rawReview['reviewDesc']
                },
                "message": "Review already exists."
            }
        ), 400
    
    
    # Insert new review into database
    newReview = data.reviews(**rawReview)
    try:
        insertResult = db.reviews.insert_one(data.asdict(newReview))

        return jsonify( 
            {   
                "code": 201,
                "data": rawReview['reviewDesc']
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingName": rawReview['reviewDesc']
                },
                "message": "An error occurred creating the listing."
            }
        ), 500

# -----------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port = 5021)