# Port: 5101
# Routes: 
# -----------------------------------------------------------------------------------------

import bson
import json
from bson import json_util
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

from bson.objectid import ObjectId

from datetime import datetime

from gridfs import GridFS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# app.config["MONGO_URI"] = "mongodb+srv://jwleong2020:uOfXCrxLPCjgyA92@greenbamboo.wbiambw.mongodb.net/GreenBamboo?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb+srv://jwleong2020:uOfXCrxLPCjgyA92@drinkx.eskadzx.mongodb.net/DrinkX?retryWrites=true&w=majority"
db = PyMongo(app).db

mongo = PyMongo(app)
fs = GridFS(mongo.db)

# -----------------------------------------------------------------------------------------
# [POST] Submit mod request
# - Submit mod request with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/submitModRequest', methods=['POST'])
def submitModRequest():
    data = request.get_json()
    print(data)
    userID = data['userID']
    drinkType = data['drinkType']
    modDesc = data['modDesc']

    try: 
        submitReq = db.modRequests.insert_one({
            'userID': ObjectId(userID),
            'drinkType': drinkType,
            'modDesc': modDesc, 
            'reviewStatus': True
        })

        return jsonify(
            {   
                "code": 201,
                "data": {
                    "userID": userID,
                    "drinkType": drinkType,
                    "modDesc": modDesc, 
                    "reviewStatus": True
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
                        "userID": userID,
                        "drinkType": drinkType,
                        "modDesc": modDesc,
                        "reviewStatus": True
                    }
                },
                "message": "An error occurred updating the mod request."
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
# [POST] Update mod request status
# - Update mod request with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/updateModRequest', methods=['POST'])
def updateModRequest():
    data = request.get_json()
    print(data)
    requestID = data['requestID']
    reviewStatus = data['reviewStatus']

    try: 
        updateReviewStatus = db.modRequests.update_one({'_id': ObjectId(requestID)}, {'$set': {'reviewStatus': reviewStatus}})

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
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5101)