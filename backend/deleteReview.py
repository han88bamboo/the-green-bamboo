# Port: 5023
# Routes: /deleteReview/<id> (DELETE)
# -----------------------------------------------------------------------------------------

import bson
import json
from bson import json_util
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

from bson.objectid import ObjectId

import data

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# app.config["MONGO_URI"] = "mongodb+srv://jwleong2020:uOfXCrxLPCjgyA92@greenbamboo.wbiambw.mongodb.net/GreenBamboo?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb+srv://jwleong2020:uOfXCrxLPCjgyA92@drinkx.eskadzx.mongodb.net/DrinkX?retryWrites=true&w=majority"
db = PyMongo(app).db

def parse_json(data):
    return json.loads(json_util.dumps(data))

# -----------------------------------------------------------------------------------------
# [DELETE] Deletes a review
# - Delete entry with specified id from the "reviews" collection.
# - Possible return codes: 201 (Deleted), 400 (Review doesn't exist), 500 (Error during deletion)
@app.route("/deleteReview/<id>", methods= ['DELETE'])
def deleteReview(id):

    # Find the review entry with the specified id
    existingReview = db.reviews.find_one({"_id": ObjectId(id)})
    if(existingReview == None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "id": id
                },
                "message": "Review doesn't exist."
            }
        ), 400
    

    # Delete the review entry with the specified id
    try:
        deleteResult = db.reviews.delete_one({"_id": ObjectId(id)})

        return jsonify( 
            {   
                "code": 200,
                "data": id
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "id": id
                },
                "message": "An error occurred deleting the listing."
            }
        ), 500

# -----------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port = 5023)