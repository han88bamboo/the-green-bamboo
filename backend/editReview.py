# Port: 5022
# Routes: /voteReview (POST)
# -----------------------------------------------------------------------------------------

import bson
import json
from bson import json_util
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

from bson.objectid import ObjectId

from gridfs import GridFS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# app.config["MONGO_URI"] = "mongodb+srv://jwleong2020:uOfXCrxLPCjgyA92@greenbamboo.wbiambw.mongodb.net/GreenBamboo?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb+srv://jwleong2020:uOfXCrxLPCjgyA92@drinkx.eskadzx.mongodb.net/DrinkX?retryWrites=true&w=majority"
db = PyMongo(app).db

mongo = PyMongo(app)
fs = GridFS(mongo.db)

# -----------------------------------------------------------------------------------------
# [POST] Vote review
# - Update review with new votes
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/voteReview', methods=['POST'])
def voteReview():
    data = request.get_json()
    print(data)
    reviewID = data['reviewID']
    userVotes = data['userVotes']

    for voteType in userVotes:
        votes = userVotes[voteType]
        for vote in votes:
            if isinstance(vote["userID"], str):
                vote["userID"] = ObjectId(vote["userID"])
            if isinstance(vote["date"], str):
                vote["date"] = datetime.strptime(vote["date"], "%Y-%m-%dT%H:%M:%S.%fZ")

    try: 
        voteReview = db.reviews.update_one({'_id': ObjectId(reviewID['$oid'])}, {'$set': {'userVotes': userVotes}})

        return jsonify(
            {   
                "code": 201,
                "data": userVotes
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "data": userVotes
                },
                "message": "An error occurred updating the image."
            }
        ), 500

# -----------------------------------------------------------------------------------------
    
# [PUT] Update review
# - Update review with review metrics
# - Possible return codes: 200 (Updated), 400(Review not found), 500 (Error during update)
@app.route('/updateReview/<id>', methods=['PUT'])
def updateReview(id):
    reviewID= ObjectId(id)
    data = request.get_json()
    existingReview = db.reviews.find_one({'_id': ObjectId(id)})
    data['reviewTarget'] = ObjectId(data['reviewTarget'])  # Convert reviewTarget to ObjectId
    data['userID'] = ObjectId(data['userID'])  # Convert userID to ObjectId

    if len(data['taggedUsers']) >0:
        temp_tag_id =[]
        for userId in data['taggedUsers']:
            temp_tag_id.append(ObjectId(userId))
        data['taggedUsers'] = temp_tag_id
    if len(data['flavorTag']) >0:
        temp_flavour_tag =[]
        for flavour_id in data['flavorTag']:
            temp_flavour_tag.append(ObjectId(flavour_id['$oid']))
        data['flavorTag'] = temp_flavour_tag

    if(existingReview == None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "listingName": data['reviewDesc']
                },
                "message": "Review does not exist."
            }
        ), 400

    try: 
        voteReview = db.reviews.update_one({'_id': reviewID}, {'$set': data})
        return jsonify(
            {   
                "code": 200,
                "data": data['reviewDesc']
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "data": data['reviewDesc']
                },
                "message": "An error occurred updating the review."
            }
        ), 500

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5022)