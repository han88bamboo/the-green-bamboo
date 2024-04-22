# Port: 5051
# Routes: /updateObservationTag (PUT)
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

from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)  # Allow all requests

load_dotenv()
app.config["MONGO_URI"] = os.getenv('MONGO_DB_URL')
db = PyMongo(app).db

mongo = PyMongo(app)
fs = GridFS(mongo.db)

# -----------------------------------------------------------------------------------------
    
# [PUT] Update review
# - Update review with review metrics
# - Possible return codes: 201 (Updated), 400(Observation tag not found), 500 (Error during update)
@app.route('/updateObservationTag', methods=['PUT'])
def updateObservationTag():
    data = request.get_json()
    # for loop for each observation tag and update
    updates = []
    for elem in data:

        existingObservationTag = db.observationTags.find_one({'_id': ObjectId(elem["_id"]["$oid"])})

        if(existingObservationTag == None):
            return jsonify(
                {   
                    "code": 400,
                    "data": {
                        "observationTag": elem['observationTag']
                    },
                    "message": "Observation Tag does not exist."
                }
            ), 400

        tag_key, tag_value = list(elem.items())[1]
        tag_dict = {"$set":{tag_key: tag_value}}
        updates.append({"filter": {"_id": ObjectId(elem["_id"]["$oid"])}, "update": tag_dict})


    try: 
        for update in updates:
            filter_criteria = update["filter"]
            update_data = update["update"]
            db.observationTags.update_many(filter_criteria, update_data)
        return jsonify(
            {   
                "code": 201,
                "data": elem['observationTag']
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "data": elem['observationTag']
                },
                "message": "An error occurred updating the observation tags."
            }
        ), 500

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5051)