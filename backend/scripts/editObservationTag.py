# Port: 5051
# Routes: /updateObservationTag (PUT)
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, request, jsonify
from bson.objectid import ObjectId

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
    
# [PUT] Update review
# - Update review with review metrics
# - Possible return codes: 201 (Updated), 400(Observation tag not found), 500 (Error during update)
@blueprint.route('/updateObservationTag', methods=['PUT'])
def updateObservationTag():
    db = g.db
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
